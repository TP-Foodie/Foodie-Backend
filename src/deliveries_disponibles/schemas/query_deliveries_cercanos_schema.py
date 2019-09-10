from marshmallow import Schema, fields, validate

from deliveries_disponibles.schemas.extra_validations import validate_coordinates

class QueryDeliveriesCercanosSchema(Schema):
    radius = fields.Int(required=True, validate=validate.Range(min=0, max=15))
    coordinates = fields.List(fields.Float, required=True, validate=validate_coordinates)

    class Meta:
        strict = True