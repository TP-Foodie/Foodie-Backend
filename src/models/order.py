from mongoengine import Document, IntField, ReferenceField, CASCADE, StringField, EmbeddedDocumentField

from src.models import User, Place


class Product(Document):
    name = StringField(max_length=150, required=True)
    place = ReferenceField(Place, required=True)


class Order(Document):
    WAITING_STATUS = "WS"
    TAKEN_STATUS = "TS"
    NORMAL_TYPE = "NT"
    FAVOR_TYPE = "FT"

    status = (WAITING_STATUS, TAKEN_STATUS)
    types = (NORMAL_TYPE, FAVOR_TYPE)

    number = IntField(required=True)
    status = StringField(choices=status, default=WAITING_STATUS)
    type = StringField(choices=types, default=NORMAL_TYPE)  # TODO: rename this
    owner = ReferenceField(User, reverse_delete_rule=CASCADE, required=True)
    product = ReferenceField(Product, reverse_delete_rule=CASCADE, required=True)
