from marshmallow import Schema, fields


class UserRatingSchema(Schema):
    description = fields.String(required=False)

    class Meta:
        fields = ('user', 'description', 'rating')
