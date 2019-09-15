from mongoengine import Document, IntField, ReferenceField

from src.models import User


class OrderType(Document):
    pass


class OrderStatus(Document):
    pass


class Order(Document):
    number = IntField
    status = ReferenceField(OrderStatus)
    type = ReferenceField(OrderType)
    owner = ReferenceField(User)

    meta = {'allow_inheritance': True}
