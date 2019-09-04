from models import FoodieModel

class QueryDeliveriesCercanos(FoodieModel):
    id_ = None
    radius = None
    coordinates = None

    def __init__(self, id_, radius, coordinates):
        self.id_ = id_
        self.radius = radius
        self.coordinates = coordinates