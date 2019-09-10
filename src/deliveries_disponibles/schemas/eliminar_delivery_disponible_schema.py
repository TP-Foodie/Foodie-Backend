from marshmallow import Schema, fields, validate

class EliminarDeliveryDisponibleSchema(Schema):
    _id = fields.Str(required=True, validate=validate.Length(min=1))

    class Meta:
        strict = True