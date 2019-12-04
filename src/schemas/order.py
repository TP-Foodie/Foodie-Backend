from marshmallow import Schema, fields

from schemas.user import UserSchema
from schemas.product_schema import ProductSchema


class OrderedProductSchema(Schema):
    product = fields.Nested(ProductSchema)

    class Meta:
        fields = ('id', 'quantity', 'product')


class ListOrderSchema(Schema):
    delivery = fields.Nested(UserSchema)

    class Meta:
        fields = ('id', 'name', 'number', 'status', 'type', 'delivery', 'id_chat', 'owner')


class DetailsOrderSchema(Schema):
    owner = fields.Nested(UserSchema)
    ordered_products = fields.List(fields.Nested(OrderedProductSchema))
    delivery = fields.Nested(UserSchema)

    class Meta:
        fields = (
            'id', 'name', 'number', 'status', 'type', 'owner', 'ordered_products',
            'delivery', 'id_chat', 'quotation', 'delivery_rated', 'owner_rated',
            'gratitude_points'
        )
