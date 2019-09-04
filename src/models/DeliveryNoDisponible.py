from models import FoodieModel

class DeliveryNoDisponible(FoodieModel):
    id_ = None

    def __init__(self, id_):
        self.id_ = id_