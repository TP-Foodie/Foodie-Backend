from models import FoodieModel


class User(FoodieModel):
    id = None
    name = None

    def __init__(self, id, name):
        self.id = id
        self.name = name
