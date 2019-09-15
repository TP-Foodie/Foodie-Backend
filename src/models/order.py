from mongoengine import Document, IntField, ReferenceField, CASCADE

from src.models import User


class OrderType(Document):
    pass


class OrderStatus(Document):
    pass


class Order(Document):
    number = IntField(required=True)
    status = ReferenceField(OrderStatus, required=True)
    type = ReferenceField(OrderType, required=True)
    owner = ReferenceField(User, reverse_delete_rule=CASCADE, required=True)

    meta = {'allow_inheritance': True}
