""" This module handles business logic of available deliveries_endpoint """

from models import User


def query_nearby_deliveries(query_data):
    """ This method handles business logic of GET in available_deliveries endpoint """
    # create geospatial query
    longitude = query_data['coordinates'][0]
    latitude = query_data['coordinates'][1]
    radius = query_data['radius']

    deliveries = User.objects(  # pylint: disable=E1101
        coordinates__geo_within_center=[[longitude, latitude], radius],
        type=User.DELIVERY_TYPE,
        available=True
    )

    return [delivery for delivery in deliveries]
