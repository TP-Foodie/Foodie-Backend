from mongoengine import Document, StringField, FloatField

class Chat(Document):
    uid_1 = StringField(required=True)
    uid_2 = StringField(required=True)
    id_order = StringField(required=True)

class ChatMessage(Document):
    uid_sender = StringField(required=True)
    message = StringField(required=True)
    timestamp = FloatField(required=True)
    id_chat = StringField(required=True)
