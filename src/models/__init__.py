from mongoengine import Document,\
    StringField,\
    EmbeddedDocumentField,\
    FloatField,\
    EmbeddedDocument,\
    EmailField, \
    BooleanField


class Coordinates(EmbeddedDocument):
    latitude = FloatField(required=True)
    longitude = FloatField(required=True)


class Place(Document):
    name = StringField(required=True)
    coordinates = EmbeddedDocumentField(Coordinates)


class User(Document):
    DELIVERY_TYPE = "DELIVERY"
    CUSTOMER_TYPE = "CUSTOMER"
    BACK_OFFICE_TYPE = "BACK_OFFICE"

    name = StringField(required=False)
    last_name = StringField(required=False)
    google_id = StringField(required=False)
    password = StringField(required=True)
    email = EmailField(required=True, unique=True)
    profile_image = StringField(required=False)
    phone = StringField(required=False)
    type = StringField(
        required=False,
        regex="CUSTOMER|DELIVERY|BACK_OFFICE")
    subscription = StringField(
        required=False,
        regex="FLAT|PREMIUM")


class Transaction(Document):
    customer_id = StringField(required=True)
    delivery_id = StringField(required=False)
    amount = FloatField(required=True)
    delivery_collected = BooleanField(required=False)
