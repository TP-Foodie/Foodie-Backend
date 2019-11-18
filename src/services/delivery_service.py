""" This module handles business logic of available deliveries_endpoint """

from models.order import Order
from repositories import user_repository
from services.exceptions.user_exceptions import NonExistingDeliveryException


def query_nearby_deliveries(query_data):
    """ This method handles business logic of GET in available_deliveries endpoint """
    # create geospatial query
    longitude = query_data['coordinates'][0]
    latitude = query_data['coordinates'][1]
    radius = query_data['radius']

    return user_repository.get_nearby_available_deliveries(
        longitude,
        latitude,
        radius)


def handle_status_change(delivery, order_status):
    if not user_repository.delivery_exists(delivery):
        raise NonExistingDeliveryException()

    if order_status == Order.TAKEN_STATUS:
        user_repository.set_delivery_as_unavailable(delivery)
    elif order_status in [Order.DELIVERED_STATUS, Order.WAITING_STATUS, Order.CANCELLED_STATUS]:
        user_repository.set_delivery_as_available(delivery)
