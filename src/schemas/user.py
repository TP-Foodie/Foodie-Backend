from marshmallow import Schema, fields
from marshmallow.validate import OneOf

from schemas.place import CoordinatesSchema


class UserSchema(Schema):
    class Meta:
        fields = ('id', 'name', 'last_name', 'email', 'profile_image', 'phone', 'type')


TYPE_VALIDATION = OneOf(choices=("CUSTOMER", "DELIVERY"))
SUBSCRIPTION_VALIDATION = OneOf(choices=("FLAT", "PREMIUM"))


class CreateUserSchema(Schema):
    name = fields.Str(required=False)
    last_name = fields.Str(required=False)
    password = fields.Str(required=True)
    email = fields.Email(required=True)
    type = fields.Str(required=False, validate=TYPE_VALIDATION)
    subscription = fields.Str(required=False, validate=SUBSCRIPTION_VALIDATION)
    phone = fields.Str(required=False)
    profile_image = fields.String(required=False)
    fcmToken = fields.String(required=False)


class UpdateUserSchema(Schema):
    name = fields.Str(required=False)
    last_name = fields.Str(required=False)
    password = fields.Str(required=False)
    email = fields.Email(required=False)
    type = fields.Str(required=False, validate=TYPE_VALIDATION)
    subscription = fields.Str(required=False, validate=SUBSCRIPTION_VALIDATION)
    phone = fields.Str(required=False)
    profile_image = fields.String(required=False)
    location = fields.Nested(CoordinatesSchema)
    balance = fields.Float()
    fcmToken = fields.String(required=False)


class UserProfile(Schema):
    class Meta:
        fields = (
            'id',
            'name',
            'last_name',
            'email',
            'profile_image',
            'type',
            'subscription',
            'reputation',
            'messages_sent',
            'phone',
            'location'
        )
