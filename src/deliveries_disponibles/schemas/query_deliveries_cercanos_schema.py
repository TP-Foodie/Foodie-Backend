from marshmallow import Schema, fields

class QueryDeliveriesCercanosSchema(Schema):
    radius = fields.Int(required=True)
    coordinates = fields.List(fields.Float, required=True)

    class Meta:
        strict = True