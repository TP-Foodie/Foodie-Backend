from marshmallow import Schema, fields


class AuthorizationSchema(Schema):
    password = fields.Str(required=True)
    email = fields.Email(required=True)


class GoogleAuthorizationSchema(Schema):
    google_token = fields.Str(required=True)
