import json
import requests
from mongoengine import Q
from models.order import Order
from repositories import order_repository, product_repository, user_repository
from services.exceptions.user_exceptions import NonExistingDeliveryException
from settings import Config


def create(order_type, owner, product):
    created_product = product_repository.get_or_create(*product.values())
    return order_repository.create(
        order_type=order_type,
        owner=owner,
        product=created_product.id,
        number=order_repository.count() + 1
    )


def take(order_id, new_data):
    delivery = new_data.get('delivery', None)
    if not user_repository.delivery_exists(delivery):
        raise NonExistingDeliveryException()

    order_repository.update(order_id, 'status', new_data.get('status', Order.WAITING_STATUS))
    return order_repository.update(order_id, 'delivery', delivery)


def placed_by(user_id, start_date=None, end_date=None):
    user_orders = order_repository.filter_by({'owner': user_id})

    return user_orders.filter(Q(created__gte=start_date) & Q(created__lte=end_date))\
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
