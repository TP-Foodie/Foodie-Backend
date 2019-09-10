from marshmallow import Schema, fields, validate

from deliveries_disponibles.schemas.extra_validations import validate_coordinates

class DeliveryDisponibleSchema(Schema):
    _id = fields.Str(required=True, validate=validate.Length(min=1))
    name = fields.Str(required=True, validate=validate.Length(min=1))
    profile_image = fields.URL(required=True, validate=validate.Length(min=1))
    coordinates = fields.List(fields.Float, required=True, validate=validate_coordinates)

    class Meta:
        strict = True