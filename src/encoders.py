from flask.json import JSONEncoder
from models import FoodieModel


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, FoodieModel):
            dictionary = obj.__dict__
            if "id_" in dictionary:
                id_ = dictionary.pop("id_")
                dictionary["id"] = id_

            for key in dictionary.keys():
                if isinstance(dictionary[key], FoodieModel):
                    dictionary[key] = self.default(dictionary[key])

            return dictionary
        return super(CustomJSONEncoder, self).default(obj)
