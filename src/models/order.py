from mongoengine import Document, IntField, ReferenceField, CASCADE, StringField

from src.models import User

class Product(Document):
    pass

class Order(Document):
    WAITING_STATUS = "WS"
    NORMAL_TYPE = "NT"
    FAVOR_TYPE = "FT"

    status = (WAITING_STATUS, )
    types = (NORMAL_TYPE, FAVOR_TYPE)

    number = IntField(required=True)
    status = StringField(choices=status, default=WAITING_STATUS)
    type = StringField(choices=types, default=NORMAL_TYPE)
    owner = ReferenceField(User, reverse_delete_rule=CASCADE, required=True)
    product = ReferenceField(Product, reverse_delete_rule=CASCADE, required=True)
