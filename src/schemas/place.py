from marshmallow import Schema, fields


class PlaceSchema(Schema):
    class Meta:
        fields = ('coordinates', 'name')