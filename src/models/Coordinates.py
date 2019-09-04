from models import FoodieModel

class Coordinates(FoodieModel):
    latitude = None
    longitude = None

    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude