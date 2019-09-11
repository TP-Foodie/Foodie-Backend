""" This module is the model that represents Query de Deliveries Cercanos """

from deliveries_disponibles.models import FoodieModel

class QueryDeliveriesCercanos(FoodieModel):
    """ Model Query Deliveries Cercanos."""
    radius = None
    coordinates = None

    def __init__(self, radius, coordinates):
        self.radius = radius
        self.coordinates = coordinates
