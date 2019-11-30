from datetime import datetime
from mongoengine import Document, \
    StringField, \
    EmbeddedDocumentField, \
    FloatField, \
    EmbeddedDocument, \
    EmailField, \
    BooleanField, IntField, DateTimeField, DateField


class Coordinates(EmbeddedDocument):
    latitude = FloatField(required=True)
    longitude = FloatField(required=True)


class User(Document):
    DELIVERY_TYPE = "DELIVERY"
    CUSTOMER_TYPE = "CUSTOMER"
    BACK_OFFICE_TYPE = "BACK_OFFICE"

    FLAT_SUBSCRIPTION = "FLAT"
    PREMIUM_SUBSCRIPTION = "PREMIUM"

    name = StringField(required=False)
    last_name = StringField(required=False)
    google_id = StringField(required=False)
    password = StringField(required=False)
    email = EmailField(required=True, unique=True)
    profile_image = StringField(required=False)
    phone = StringField(required=False)
    type = StringField(
        required=False,
        regex="CUSTOMER|DELIVERY|BACK_OFFICE")
    subscription = StringField(
        required=False,
        regex="FLAT|PREMIUM",
        default="FLAT")
    recovery_token = StringField(required=False)
    recovery_token_date = DateTimeField(required=False)
    reputation = FloatField(default=2.5)
    fcmToken = StringField(required=False)
    messages_sent = IntField(default=0)
    created = DateField(default=datetime.now().date())
    balance = FloatField(default=0)
    location = EmbeddedDocumentField(Coordinates)
    available = BooleanField(default=True)
    deliveries_completed = IntField(default=0)
    gratitude_points = IntField(default=0)


class Transaction(Document):
    customer_id = StringField(required=True)
    delivery_id = StringField(required=False)
    amount = FloatField(required=True)
    delivery_collected = BooleanField(required=False)
