from deliveries_disponibles.models import FoodieModel

class DeliveryDisponible(FoodieModel):
    _id = None
    name = None
    profile_image = None
    coordinates = None

    def __init__(self, _id, name, profile_image, coordinates):
        self._id = _id
        self.name = name
        self.profile_image = profile_image
        self.coordinates = coordinates