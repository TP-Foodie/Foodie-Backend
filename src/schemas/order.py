from marshmallow import Schema, fields

from schemas.place import PlaceSchema
from schemas.user import UserSchema
from schemas.chat_schema import CreateChatSchema


class ProductSchema(Schema):
    place = fields.Nested(PlaceSchema)

    class Meta:
        fields = ('name', 'place')


class ListOrderSchema(Schema):
    delivery = fields.Nested(UserSchema)

    class Meta:
        fields = ('id', 'number', 'status', 'type', 'delivery')


class DetailsOrderSchema(Schema):
    owner = fields.Nested(UserSchema)
    product = fields.Nested(ProductSchema)
    delivery = fields.Nested(UserSchema)
    chat = fields.Nested(CreateChatSchema)

    class Meta:
        fields = ('id', 'number', 'status', 'type', 'owner', 'product', 'delivery', 'chat')
