""" This module representes extra validations for Marshmallow schemas """

from marshmallow import ValidationError


# Mongo says:
# Valid longitude values are between -180 and 180, both inclusive.
# Valid latitude values are between -90 and 90, both inclusive.


def validate_coordinates(coordinates):
    """ This method validates geospatial coordinates """
    if coordinates is None:
        raise ValidationError("Coordinates is None.")
    if len(coordinates) != 2:
        raise ValidationError("Coordinates lenght must be 2.")
    if (coordinates[0] > 180 or coordinates[0] < -180):
        raise ValidationError(
            "Valid longitude values are between -180 and 180, both inclusive.")
    if (coordinates[1] > 90 or coordinates[1] < -90):
        raise ValidationError(
            "Valid latitude values are between -90 and 90, both inclusive.")
    return True
