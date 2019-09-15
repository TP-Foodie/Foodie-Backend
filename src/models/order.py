from mongoengine import Document, IntField


class Order(Document):
    number = IntField


