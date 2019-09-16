""" This module is the model that represents the Query of Nearby Deliveries. """

from models import FoodieModel

class QueryNearbyDeliveries(FoodieModel):
    """ Model Query Nearby Deliveries."""
    radius = None
    coordinates = None

    def __init__(self, radius, coordinates):
        self.radius = radius
        self.coordinates = coordinates
