from marshmallow import Schema, fields

class BorrarDeliveryDisponibleSchema(Schema):
    _id = fields.Str(required=True)

    class Meta:
        strict = True