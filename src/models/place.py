from models import FoodieModel


class Place(FoodieModel):
    name = None
    coordinates = None

    def __init__(self, _id, name, coordinates):
        self._id = _id
        self.name = name
        self.coordinates = coordinates


class Coordinates(FoodieModel):
    latitude = None
    longitude = None

    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
