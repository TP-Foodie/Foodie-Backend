from deliveries_disponibles.models import FoodieModel

class EliminarDeliveryDisponible(FoodieModel):
    """ Model Eliminar Delivery Disponible."""
    _id = None

    def __init__(self, _id):
        self._id = _id
