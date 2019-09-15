from mongoengine import Document, IntField, ReferenceField


class OrderType(Document):
    pass


class OrderStatus(Document):
    pass


class Order(Document):
    number = IntField
    status = ReferenceField(OrderStatus)
    type = ReferenceField(OrderType)

    meta = {'allow_inheritance': True}
