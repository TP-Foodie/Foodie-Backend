""" This module is the Marshmallow Schema for QueryNearbyDeliveries """

from marshmallow import Schema, fields, validate

from schemas.extra_validations import validate_coordinates


class QueryNearbyDeliveriesSchema(Schema):
    """ This class is the Marshmallow Schema for QueryNearbyDeliveries """
    radius = fields.Int(required=True, validate=validate.Range(min=0, max=15))
    coordinates = fields.List(
        fields.Float,
        required=True,
        validate=validate_coordinates)
