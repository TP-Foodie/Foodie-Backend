from models import FoodieModel

class DeliveryDisponible(FoodieModel):
    id_ = None
    name = None
    profile_image = None
    coordinates = None

    def __init__(self, id_, name, profile_image, coordinates):
        self.id_ = id_
        self.name = name
        self.profile_image = profile_image
        self.coordinates = coordinates