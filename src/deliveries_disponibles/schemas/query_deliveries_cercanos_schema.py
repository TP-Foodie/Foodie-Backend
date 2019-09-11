""" This module is the Marshmallow Schema for QueryDeliveriesCercanos """

from marshmallow import Schema, fields, validate, post_load

from deliveries_disponibles.models.query_deliveries_cercanos import QueryDeliveriesCercanos
from deliveries_disponibles.schemas.extra_validations import validate_coordinates

class QueryDeliveriesCercanosSchema(Schema):
    """ This class is the Marshmallow Schema for QueryDeliveriesCercanos """
    radius = fields.Int(required=True, validate=validate.Range(min=0, max=15))
    coordinates = fields.List(fields.Float, required=True, validate=validate_coordinates)

    class Meta:
        """ Clase que pide Marshmallow para que el schema sea estricto """
        strict = True

    @post_load
    def make_query_deliveries_cercanos(self, data, **kwargs):
        """ This method tells load() return QueryDeliveriesCercanos """
        return QueryDeliveriesCercanos(**data)
        