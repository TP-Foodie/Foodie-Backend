from marshmallow import Schema, fields

from src.schemas.place import PlaceSchema
from src.schemas.user import UserSchema


class ProductSchema(Schema):
    place = fields.Nested(PlaceSchema)

    class Meta:
        fields = ('name', 'place')


class ListOrderSchema(Schema):
    class Meta:
        fields = ('id', 'number', 'status', 'type')


class DetailsOrderSchema(Schema):
    owner = fields.Nested(UserSchema)
    product = fields.Nested(ProductSchema)

    class Meta:
        fields = ('id', 'number', 'status', 'type', 'owner', 'product')
