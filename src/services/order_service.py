import json
import requests
from mongoengine import Q

from repositories import order_repository, product_repository, user_repository
from services import delivery_service
from services.exceptions.user_exceptions import NonExistingDeliveryException
from services.rule_service import RuleService
from settings import Config
from models.order import Order


DELIVERY_PERCENTAGE = 0.85
rule_service = RuleService()  # pylint: disable=invalid-name


def create(order_type, product, payment_method, owner):
    created_product = product_repository.get_or_create(*product.values())
    return order_repository.create(
        order_type=order_type,
        owner=owner,
        product=created_product.id,
        payment_method=payment_method,
        number=order_repository.count() + 1
    )


def update(order_id, data):
    if data.get('delivery'):
        return take(order_id, data.get('delivery'))

    if data.get('status', '') in Order.CANCELLED_STATUS:
        return cancel(order_id)

    if data.get('status') == Order.DELIVERED_STATUS:
        return deliver(order_id)

    if data.get('status') == Order.WAITING_STATUS:
        return unassign(order_id)

    return order_repository.update(order_id, data)


def take(order_id, delivery):
    if not user_repository.delivery_exists(delivery):
        raise NonExistingDeliveryException()

    delivery_service.handle_status_change(delivery, Order.TAKEN_STATUS)

    return order_repository.update(
        order_id,
        {
            'delivery': delivery,
            'status': Order.TAKEN_STATUS,
            'quotation': rule_service.quote_price(order_id)
        }
    )


def deliver(order_id):
    order = order_repository.get_order(order_id)

    user_repository.increment_deliveries_completed(str(order.owner.id))
    user_repository.increment_deliveries_completed(str(order.delivery.id))

    delivery_service.handle_status_change(order.delivery.id, Order.DELIVERED_STATUS)
    user_repository.update(order.delivery.id, {'balance': order.quotation * DELIVERY_PERCENTAGE})

    return order_repository.update(order_id, {'status': Order.DELIVERED_STATUS})


def cancel(order_id):
    unassign(order_id, Order.CANCELLED_STATUS)


def unassign(order_id, status=Order.WAITING_STATUS):
    order = order_repository.get_order(order_id)
    delivery_service.handle_status_change(order.delivery.id, status)
    return order_repository.update(order_id, {'status': status, 'delivery': None})


def placed_by(user_id, start_date=None, end_date=None):
    user_orders = order_repository.filter_by({'owner': user_id})

    return user_orders.filter(Q(created__gte=start_date) & Q(created__lte=end_date)) \
        if start_date and end_date else user_orders


def distance(order):
    owner_latitude = order.owner.location.latitude
    owner_longitude = order.owner.location.longitude

    product_latitude = order.product.place.coordinates.latitude
    product_longitude = order.product.place.coordinates.longitude

    key = Config.MAP_QUEST_API_KEY
    from_location = json.dumps({'latLng': {
        'lat': product_latitude,
        'lng': product_longitude
    }})
    to_location = json.dumps({'latLng': {
        'lat': owner_latitude,
        'lng': owner_longitude
    }})

    url = 'http://www.mapquestapi.com/directions/v2/route?key={}&from={}&to={}&unit=k'.format(
        key, from_location, to_location
    )
    response = requests.get(url)

    return float(json.loads(response.content)['route']['distance'])


def count_for_user(user_id):
    return order_repository.count_for_user(user_id)


def order_position(order):
    owner_latitude = order.owner.location.latitude
    owner_longitude = order.owner.location.longitude

    key = Config.MAP_QUEST_API_KEY
    url = 'http://open.mapquestapi.com/geocoding/v1/reverse?key={}&location={},{}'.format(
        key, owner_latitude, owner_longitude
    )

    response = requests.get(url)

    return json.loads(response.content)['results'][0]['locations'][0]['adminArea5'].lower()
