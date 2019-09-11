""" This module is the Marshmallow Schema for DeliveryDisponible """

from marshmallow import Schema, fields, validate, post_load

from models.delivery_disponible import DeliveryDisponible
from schemas.extra_validations import validate_coordinates

class DeliveryDisponibleSchema(Schema):
    """ This class is the Marshmallow Schema for DeliveryDisponible """
    _id = fields.Str(required=True, validate=validate.Length(min=1))
    name = fields.Str(required=True, validate=validate.Length(min=1))
    profile_image = fields.URL(required=True, validate=validate.Length(min=1))
    coordinates = fields.List(fields.Float, required=True, validate=validate_coordinates)

    class Meta:
        """ Clase que pide Marshmallow para que el schema sea estricto """
        strict = True

    @post_load
    def make_delivery_disponible(self, data, **kwargs):
        """ This method tells load() return DeliveryDisponible """
        return DeliveryDisponible(**data)
