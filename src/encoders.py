from unittest.mock import MagicMock
from flask.json import JSONEncoder
from bson import ObjectId
from models import FoodieModel

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):  # pylint: disable=E0202, W0221

        if isinstance(obj, FoodieModel):
            dictionary = obj.__dict__
            if "id_" in dictionary:
                id_ = dictionary.pop("id_")
                dictionary["id"] = id_

            for key in dictionary.keys():
                if isinstance(dictionary[key], FoodieModel):
                    dictionary[key] = self.default(dictionary[key])

            return dictionary

        if isinstance(obj, ObjectId):
            return str(obj)

        if isinstance(obj, MagicMock):
            return "serializable for test"

        return super(CustomJSONEncoder, self).default(obj)
