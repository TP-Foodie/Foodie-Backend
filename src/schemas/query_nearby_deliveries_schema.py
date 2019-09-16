""" This module is the Marshmallow Schema for QueryNearbyDeliveries """

from marshmallow import Schema, fields, validate, post_load

from models.query_nearby_deliveries import QueryNearbyDeliveries
from schemas.extra_validations import validate_coordinates

class QueryNearbyDeliveriesSchema(Schema):
    """ This class is the Marshmallow Schema for QueryNearbyDeliveries """
    radius = fields.Int(required=True, validate=validate.Range(min=0, max=15))
    coordinates = fields.List(fields.Float, required=True, validate=validate_coordinates)

    class Meta:
        """ Clase que pide Marshmallow para que el schema sea estricto """
        strict = True

    @post_load
    def make_query_nearby_deliveries(self, data, **kwargs):
        """ This method tells load() return QueryNearbyDeliveries """
        return QueryNearbyDeliveries(**data)
        