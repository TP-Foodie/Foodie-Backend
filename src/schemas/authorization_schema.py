from marshmallow import Schema, fields


class AuthorizationSchema(Schema):
    password = fields.Str(required=True)
    email = fields.Email(required=True)


class GoogleAuthorizationSchema(Schema):
    google_token = fields.Str(required=True)


class RecoveryTokenSchema(Schema):
    email = fields.Str(required=True)


class UpdatePasswordSchema(Schema):
    email = fields.Str(required=True)
    recovery_token = fields.Str(required=True)
    password = fields.Str(required=True)
