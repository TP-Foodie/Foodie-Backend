from bson import ObjectId
from marshmallow import Schema, fields, post_load


class UserFieldRatingSchema(Schema):
    id = fields.String()

    class Meta:
        fields = ('id', )


class ListUserRatingSchema(Schema):
    user = fields.Nested(UserFieldRatingSchema)
    id = fields.String()

    class Meta:
        fields = ('id', 'user', 'description', 'rating')


class CreateUserRatingSchema(Schema):
    description = fields.String(required=False)

    class Meta:
        fields = ('user', 'description', 'rating')

    @post_load
    def make_data(self, data, **kwargs):
        data['user'] = ObjectId(data['user'])
        return data
