from mongoengine import Document, IntField, ReferenceField, CASCADE

from src.models import User


class OrderType(Document):
    meta = {'allow_inheritance': True}


class OrderNormalType(OrderType):
    pass


class OrderStatus(Document):
    meta = {'allow_inheritance': True}


class OrderWaitingStatus(OrderStatus):
    pass


class Order(Document):
    number = IntField(required=True)
    status = ReferenceField(OrderStatus, required=True, default=OrderWaitingStatus)
    type = ReferenceField(OrderType, required=True, default=OrderNormalType)
    owner = ReferenceField(User, reverse_delete_rule=CASCADE, required=True)
