from mongoengine import Document, StringField, EmbeddedDocumentField, FloatField, EmbeddedDocument


class Coordinates(EmbeddedDocument):
    latitude = FloatField(required=True)
    longitude = FloatField(required=True)


class Place(Document):
    name = StringField(required=True)
    coordinates = EmbeddedDocumentField(Coordinates)
