from mongoengine import Document, \
    StringField, \
    EmbeddedDocumentField

from models import Coordinates


class Place(Document):
    name = StringField(required=True)
    coordinates = EmbeddedDocumentField(Coordinates)
    image = StringField(default="", required=False)
