from marshmallow import Schema, fields

from src.schemas.user import UserSchema


class OrderSchema(Schema):
    owner = fields.Nested(UserSchema)

    class Meta:
        fields = ('number', 'status', 'type', 'owner')


orders_schema = OrderSchema(many=True)
