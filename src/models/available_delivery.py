""" This module is the model that represents Available Delivery. """

from models import FoodieModel

class AvailableDelivery(FoodieModel):
    """ Model Available Delivery."""
    _id = None
    name = None
    profile_image = None
    coordinates = None

    def __init__(self, _id, name, profile_image, coordinates):
        self._id = _id
        self.name = name
        self.profile_image = profile_image
        self.coordinates = coordinates

    def get_id(self):
        """ Getter id """
        return self._id
