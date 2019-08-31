from models import FoodieModel


class Place(FoodieModel):
    id_ = None
    name = None
    coordinates = None

    def __init__(self, id_, name, coordinates):
        self.id_ = id_
        self.name = name
        self.coordinates = coordinates


class Coordinates(FoodieModel):
    latitude = None
    longitude = None

    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
