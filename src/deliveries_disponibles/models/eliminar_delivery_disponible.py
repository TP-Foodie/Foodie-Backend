""" This module is the model that represents Eliminar Delivery Disponible """

from deliveries_disponibles.models import FoodieModel

class EliminarDeliveryDisponible(FoodieModel):
    """ Model Eliminar Delivery Disponible."""
    _id = None

    def __init__(self, _id):
        self._id = _id

    def get_id(self):
        """ Getter id """
        return self._id
