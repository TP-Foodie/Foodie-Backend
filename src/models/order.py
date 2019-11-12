from datetime import datetime
from mongoengine import Document, IntField, ReferenceField, \
    CASCADE, StringField, NULLIFY, DateTimeField

from models import User, Place
from models.rule import RuleCondition


class Product(Document):
    name = StringField(max_length=150, required=True)
    place = ReferenceField(Place, required=True)


class Order(Document):
    WAITING_STATUS = "WS"
    TAKEN_STATUS = "TS"
    DELIVERED_STATUS = "DS"
    NORMAL_TYPE = "NT"
    FAVOR_TYPE = "FT"

    status = (WAITING_STATUS, TAKEN_STATUS, DELIVERED_STATUS)
    types = (NORMAL_TYPE, FAVOR_TYPE)

    number = IntField(required=True)
    status = StringField(choices=status, default=WAITING_STATUS)
    type = StringField(choices=types, default=NORMAL_TYPE)
    owner = ReferenceField(User, reverse_delete_rule=CASCADE, required=True)
    product = ReferenceField(Product, reverse_delete_rule=CASCADE, required=True)
    delivery = ReferenceField(User, reverse_delete_rule=NULLIFY)
    created = DateTimeField(default=datetime.now())
    date = DateTimeField(default=datetime.now())
    payment_method = StringField(
        choices=RuleCondition.PAYMENT_METHODS, default=RuleCondition.CASH_PAYMENT_METHOD
    )
    id_chat = StringField(default="")
