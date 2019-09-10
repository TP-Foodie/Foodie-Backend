from mongoengine import Document, StringField, EmbeddedDocumentField, FloatField, EmbeddedDocument, EmailField


class Coordinates(EmbeddedDocument):
    latitude = FloatField(required=True)
    longitude = FloatField(required=True)


class Place(Document):
    name = StringField(required=True)
    coordinates = EmbeddedDocumentField(Coordinates)


class User(Document):
    name = StringField(required=True)
    last_name = StringField(required=True)
    password = StringField(required=True)
    email = EmailField(required=True)
    profile_image = StringField(required=False)
