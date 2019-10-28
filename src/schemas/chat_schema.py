from marshmallow import Schema, fields

class CreateChatSchema(Schema):
    uid_1 = fields.Str(required=True)
    uid_2 = fields.Str(required=True)
    id_order = fields.Str(required=True)