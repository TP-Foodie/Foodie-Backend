from marshmallow import Schema, fields

from src.schemas.user import UserSchema


class OrderSchema(Schema):
    owner = fields.Nested(UserSchema)

    class Meta:
        fields = ('id', 'number', 'status', 'type')


orders_schema = OrderSchema(many=True)
