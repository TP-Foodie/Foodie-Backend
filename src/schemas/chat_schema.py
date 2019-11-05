from marshmallow import Schema, fields


class CreateChatSchema(Schema):
    uid_1 = fields.Str(required=True)
    uid_2 = fields.Str(required=True)
    id_order = fields.Str(required=True)


class CreateChatMessageSchema(Schema):
    uid_sender = fields.Str(required=True)
    message = fields.Str(required=True)
    timestamp = fields.Float(required=True)
