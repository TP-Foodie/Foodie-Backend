""" This module is the model that represents the Query of Nearby Deliveries. """

from mongoengine import IntField, PointField

class QueryNearbyDeliveries:
    """ Model Query Nearby Deliveries."""
    radius = IntField(required=True)
    coordinates = PointField(required=True)
