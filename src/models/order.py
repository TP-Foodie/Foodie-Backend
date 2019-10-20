from datetime import datetime
from mongoengine import Document, IntField, ReferenceField, CASCADE, StringField, NULLIFY, DateField

from models import User, Place


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
    type = StringField(choices=types, default=NORMAL_TYPE)
    owner = ReferenceField(User, reverse_delete_rule=CASCADE, required=True)
    product = ReferenceField(Product, reverse_delete_rule=CASCADE, required=True)
    delivery = ReferenceField(User, reverse_delete_rule=NULLIFY)
    date = DateField(default=datetime.now().date())
