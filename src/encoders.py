from flask.json import JSONEncoder
from bson import ObjectId
from mongoengine import Document, EmbeddedDocument
from mongoengine.base import BaseDocument


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):  # pylint: disable=E0202, W0221
        if isinstance(obj, BaseDocument):
            return obj._data

        if isinstance(obj, ObjectId):
            return str(obj)

        return super(CustomJSONEncoder, self).default(obj)
