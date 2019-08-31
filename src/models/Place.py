from models import FoodieModel


class Place(FoodieModel):
    id = None
    name = None
    coordinates = None

    def __init__(self, id, name, coordinates):
        self.id = id
        self.name = name
        self.coordinates = coordinates


class Coordinates(FoodieModel):
    latitude = None
    longitude = None

    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
