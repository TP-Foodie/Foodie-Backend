from marshmallow import Schema


class PlaceSchema(Schema):
    class Meta:
        fields = ('coordinates', 'name', 'image')


class CoordinatesSchema(Schema):
    class Meta:
        fields = ('latitude', 'longitude')
