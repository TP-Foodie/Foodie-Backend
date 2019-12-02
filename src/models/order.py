from datetime import datetime
from mongoengine import Document, IntField, ReferenceField, \
    CASCADE, StringField, NULLIFY, DateTimeField, FloatField, \
    EmbeddedDocumentField, ListField, EmbeddedDocument, BooleanField

from models import User
from models.rule import RuleCondition
from models.product import Product


class OrderedProduct(EmbeddedDocument):
    quantity = IntField(required=True)
    product = ReferenceField(Product, required=True)


class Order(Document):
    WAITING_STATUS = "WS"
    TAKEN_STATUS = "TS"
    DELIVERED_STATUS = "DS"
    CANCELLED_STATUS = "CS"
    NORMAL_TYPE = "NT"
    FAVOR_TYPE = "FT"

    status = (WAITING_STATUS, TAKEN_STATUS, DELIVERED_STATUS, CANCELLED_STATUS)
    types = (NORMAL_TYPE, FAVOR_TYPE)

    name = StringField(required=True)
    number = IntField(required=True)
    status = StringField(choices=status, default=WAITING_STATUS)
    type = StringField(choices=types, default=NORMAL_TYPE)
    owner = ReferenceField(User, reverse_delete_rule=CASCADE, required=True)
    ordered_products = ListField(EmbeddedDocumentField(OrderedProduct))
    delivery = ReferenceField(User, reverse_delete_rule=NULLIFY)
    created = DateTimeField(default=datetime.now())
    date = DateTimeField(default=datetime.now())
    payment_method = StringField(
        choices=RuleCondition.PAYMENT_METHODS, default=RuleCondition.CASH_PAYMENT_METHOD
    )
    id_chat = StringField(default="")
    gratitude_points = IntField(default=0)
    quotation = FloatField(required=False, default=0)
    completed_date = DateTimeField()
    delivery_rated = BooleanField(default=False)
    owner_rated = BooleanField(default=False)
