from geopy.distance import geodesic
from models.order import Order
from repositories import order_repository, product_repository, user_repository
from services.exceptions.user_exceptions import NonExistingDeliveryException


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


def distance(order):
    owner_latitude = order.owner.location.latitude
    owner_longitude = order.owner.location.longitude

    product_latitude = order.product.place.coordinates.latitude
    product_longitude = order.product.place.coordinates.longitude

    return geodesic(
        (owner_longitude, owner_latitude),
        (product_longitude, product_latitude)
    ).km
