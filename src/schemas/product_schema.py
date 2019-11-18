from marshmallow import Schema, fields

from schemas.place import PlaceSchema


class ProductSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    price = fields.Int(required=True)
    place = fields.Nested(PlaceSchema, required=True)
    image = fields.String(required=False)
