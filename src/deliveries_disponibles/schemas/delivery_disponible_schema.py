from marshmallow import Schema, fields

class DeliveryDisponibleSchema(Schema):
    _id = fields.Str(required=True)
    name = fields.Str(required=True)
    profile_image = fields.Str(required=True)
    coordinates = fields.List(fields.Float, required=True)

    class Meta:
        strict = True