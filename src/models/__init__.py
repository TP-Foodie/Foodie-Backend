from mongoengine import Document, \
    StringField, \
    EmbeddedDocumentField, \
    FloatField, \
    EmbeddedDocument, \
    EmailField, \
    BooleanField, IntField


class Coordinates(EmbeddedDocument):
    latitude = FloatField(required=True)
    longitude = FloatField(required=True)


class Place(Document):
    name = StringField(required=True)
    coordinates = EmbeddedDocumentField(Coordinates)


class User(Document):
    DELIVERY_TYPE = "DELIVERY"
    CUSTOMER_TYPE = "CUSTOMER"

    name = StringField(required=False)
    last_name = StringField(required=False)
    password = StringField(required=True)
    email = EmailField(required=True, unique=True)
    profile_image = StringField(required=False)
    phone = StringField(required=False)
    type = StringField(
        required=True,
        regex="CUSTOMER|DELIVERY")  # CUSTOMER, DELIVERY
    reputation = IntField(default=0)


class Transaction(Document):
    customer_id = StringField(required=True)
    delivery_id = StringField(required=False)
    amount = FloatField(required=True)
    delivery_collected = BooleanField(required=False)
