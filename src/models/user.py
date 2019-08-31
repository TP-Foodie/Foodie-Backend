from models import FoodieModel


class User(FoodieModel):
    id_ = None
    name = None

    def __init__(self, id_, name):
        self.id_ = id_
        self.name = name
