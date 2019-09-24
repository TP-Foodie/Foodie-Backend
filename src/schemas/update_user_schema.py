from marshmallow import Schema, fields
from marshmallow.validate import OneOf


class UpdateUserSchema(Schema):
    name = fields.Str(required=False)
    last_name = fields.Str(required=False)
    password = fields.Str(required=False)
    email = fields.Email(required=False)
    type = fields.Str(
        required=False,
        validate=OneOf(
            choices=(
                "CUSTOMER",
                "DELIVERY")))
    phone = fields.Str(required=False)
    profile_image = fields.String(required=False)