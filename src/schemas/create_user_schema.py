from marshmallow import Schema, fields
from marshmallow.validate import OneOf


class CreateUserSchema(Schema):
    name = fields.Str(required=False)
    last_name = fields.Str(required=False)
    password = fields.Str(required=True)
    email = fields.Email(required=True)
    type = fields.Str(
        required=True,
        validate=OneOf(
            choices=(
                "CUSTOMER",
                "DELIVERY")))
    phone = fields.Str(required=False)
    profile_image = fields.String(required=False)