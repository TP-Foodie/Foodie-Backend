from marshmallow import Schema, fields


class UserSchema(Schema):
    name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    password = fields.Str(required=True)
    email = fields.Email(required=True)
    profile_image = fields.String(required=False)