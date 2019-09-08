from deliveries_disponibles.models import FoodieModel

class BorrarDeliveryDisponible(FoodieModel):
    _id = None

    def __init__(self, _id):
        self._id = _id