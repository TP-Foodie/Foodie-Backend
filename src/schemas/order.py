from marshmallow import Schema, fields

from src.schemas.user import UserSchema


class ListOrderSchema(Schema):
    class Meta:
        fields = ('id', 'number', 'status', 'type')


orders_schema = ListOrderSchema(many=True)


class DetailsOrderSchema(Schema):
    owner = fields.Nested(UserSchema)

    class Meta:
        fields = ('id', 'number', 'status', 'type', 'owner')


order_schema = DetailsOrderSchema()
