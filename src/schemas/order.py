from marshmallow import Schema, fields

from schemas.place import PlaceSchema
from schemas.user import UserSchema


class ProductSchema(Schema):
    place = fields.Nested(PlaceSchema)

    class Meta:
        fields = ('name', 'place')


class ListOrderSchema(Schema):
    delivery = fields.Nested(UserSchema)

    class Meta:
        fields = ('id', 'number', 'status', 'type', 'delivery', 'id_chat')


class DetailsOrderSchema(Schema):
    owner = fields.Nested(UserSchema)
    product = fields.Nested(ProductSchema)
    delivery = fields.Nested(UserSchema)

    class Meta:
        fields = ('id', 'number', 'status', 'type', 'owner', 'product', 'delivery', 'id_chat', 'quotation')
