from mongoengine import Document, fields, CASCADE

from models import User


class UserRating(Document):
    user = fields.ReferenceField(User, reverse_delete_rule=CASCADE)
    description = fields.StringField(max_length=300)
    rating = fields.IntField(choices=[1, 2, 3, 4, 5], default=1)
