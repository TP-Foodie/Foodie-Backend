""" This module is the model that represents Available Delivery. """

from mongoengine import Document, StringField, ListField, FloatField


class AvailableDelivery(Document):
    """ Model Available Delivery."""
    _id = StringField(required=True, primary_key=True)
    name = StringField(required=True)
    profile_image = StringField(required=True)
    coordinates = ListField(field=FloatField(), required=True)
