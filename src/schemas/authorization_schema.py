from marshmallow import Schema, fields


class AuthorizationSchema(Schema):
    password = fields.Str(required=True)
    email = fields.Email(required=True)