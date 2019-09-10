from marshmallow import Schema, fields, validate, post_load

from deliveries_disponibles.models.query_deliveries_cercanos import QueryDeliveriesCercanos
from deliveries_disponibles.schemas.extra_validations import validate_coordinates

class QueryDeliveriesCercanosSchema(Schema):
    radius = fields.Int(required=True, validate=validate.Range(min=0, max=15))
    coordinates = fields.List(fields.Float, required=True, validate=validate_coordinates)

    class Meta:
        strict = True

    @post_load
    def make_query_deliveries_cercanos(self, data, **kwargs):
        return QueryDeliveriesCercanos(**data)