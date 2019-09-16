""" This module is the model that represents Delete Available Delivery. """

from models import FoodieModel

class DeleteAvailableDelivery(FoodieModel):
    """ Model Eliminar Delivery Disponible."""
    _id = None

    def __init__(self, _id):
        self._id = _id

    def get_id(self):
        """ Getter id """
        return self._id
