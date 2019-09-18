""" This module is the Marshmallow Schema for AvailableDelivery """

from marshmallow import Schema, fields, validate

from schemas.extra_validations import validate_coordinates

class AvailableDeliverySchema(Schema):
    """ This class is the Marshmallow Schema for AvailableDelivery """
    _id = fields.Str(required=True, validate=validate.Length(min=1))
    name = fields.Str(required=True, validate=validate.Length(min=1))
    profile_image = fields.URL(required=True, validate=validate.Length(min=1))
    coordinates = fields.List(fields.Float, required=True, validate=validate_coordinates)
