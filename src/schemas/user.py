from marshmallow import Schema


class UserSchema(Schema):
    class Meta:
        fields = ('name', 'last_name', 'email', 'profile_image', 'phone')
