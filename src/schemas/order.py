from marshmallow import Schema, fields

from src.schemas.user import UserSchema


class ListOrderSchema(Schema):
    class Meta:
        fields = ('id', 'number', 'status', 'type')


class DetailsOrderSchema(Schema):
    owner = fields.Nested(UserSchema)

    class Meta:
        fields = ('id', 'number', 'status', 'type', 'owner')
