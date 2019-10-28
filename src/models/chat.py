from mongoengine import Document, \
    StringField

class Chat(Document):
    uid_1 = StringField(required=True)
    uid_2 = StringField(required=True)
    id_order = StringField(required=True)