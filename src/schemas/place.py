from marshmallow import Schema


class PlaceSchema(Schema):
    class Meta:
        fields = ('coordinates', 'name')
