from marshmallow import Schema, fields

from schemas.place import PlaceSchema


class ListProductSchema(Schema):
    place = fields.Nested(PlaceSchema)

    class Meta:
        fields = ('id', 'name', 'description', 'price', 'place', 'image')


class ProductSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    price = fields.Int(required=True)
    place = fields.Nested(PlaceSchema, required=True)
    image = fields.String(required=False)

    class Meta:
        fields = ('id', 'name', 'description', 'price', 'place', 'image')
