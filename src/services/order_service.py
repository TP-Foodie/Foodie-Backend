import json
import requests
from mongoengine import Q

from models.order import Order
from repositories import order_repository, product_repository
from services import delivery_service
from settings import Config


def create(order_type, product, payment_method, owner):
    created_product = product_repository.get_or_create(*product.values())
    return order_repository.create(
        order_type=order_type,
        owner=owner,
        product=created_product.id,
        payment_method=payment_method,
        number=order_repository.count() + 1
    )

def handle_status_change(order_id, new_status, new_data):
    new_delivery = new_data.get('delivery', None)
    old_delivery = order_repository.get_order(order_id).delivery
    if new_status == Order.TAKEN_STATUS:
        delivery_service.handle_status_change(new_delivery, new_status)
    elif new_status == Order.DELIVERED_STATUS:
        delivery_service.handle_status_change(old_delivery.id, new_status)
    else:
        delivery_service.handle_status_change(old_delivery.id, new_status)
        order_repository.update(order_id, 'delivery', None)
        order_repository.update(order_id, 'quotation', None)

def take(order_id, new_data):
    if new_data.get('status') is not None:
        order_repository.update(order_id, 'status', new_data.get('status'))
        handle_status_change(order_id, new_data.get('status'), new_data)
        
    if new_data.get('payment_method') is not None:
        order_repository.update(order_id, 'payment_method', new_data.get('payment_method'))

    if new_data.get('delivery') is not None:
        order_repository.update(order_id, 'delivery', new_data.get('delivery'))

    if new_data.get('id_chat', None) is not None:
        order_repository.update(order_id, 'id_chat', new_data.get('id_chat'))

    if new_data.get('quotation', None) is not None:
        order_repository.update(order_id, 'quotation', new_data.get('quotation'))

    return order_repository.get_order(order_id)


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
