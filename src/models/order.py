from mongoengine import Document, IntField, StringField


class Order(Document):
    number = IntField
    status = StringField(max_length=10)
