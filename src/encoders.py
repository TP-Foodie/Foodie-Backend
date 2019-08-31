from flask.json import JSONEncoder
from models import FoodieModel


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, FoodieModel):
            return obj.__dict__
        return super(CustomJSONEncoder, self).default(obj)
