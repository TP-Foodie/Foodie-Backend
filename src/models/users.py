from mongoengine import StringField, Document, EmailField, BinaryField


class Users(Document):
    name = StringField(required=True)
    last_name = StringField(required=True)
    password = StringField(required=True)
    email = EmailField(required=True)
    profile_image = StringField(required=False)
