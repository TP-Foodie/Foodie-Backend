from mongoengine import Document, IntField, ReferenceField, StringField

from models.place import Place


class Product(Document):
    name = StringField(required=True)
    description = StringField(required=True)
    price = IntField(required=True)
    place = ReferenceField(Place, required=True)
    image = StringField(required=False)
