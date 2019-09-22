""" This module is the Marshmallow Schema for DeleteAvailableDelivery """

from marshmallow import Schema, fields, validate


class DeleteAvailableDeliverySchema(Schema):
    """ This class is the Marshmallow Schema for DeleteAvailableDelivery """
    _id = fields.Str(required=True, validate=validate.Length(min=1))
