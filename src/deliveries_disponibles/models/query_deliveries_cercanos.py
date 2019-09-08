from deliveries_disponibles.models import FoodieModel

class QueryDeliveriesCercanos(FoodieModel):
    radius = None
    coordinates = None

    def __init__(self, radius, coordinates):
        self.radius = radius
        self.coordinates = coordinates