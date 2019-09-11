""" This module is for testing extra_validations, function defined in
deliveries_disponible/schemas/extra_validations """

import unittest
from marshmallow import ValidationError

from schemas.extra_validations import validate_coordinates

class ExtraValidationsTestCase(unittest.TestCase):
    """ This class is the test case for extra_validations """

    #
    #   Success Tests
    #

    def test_success_valid_coordinates(self):
        """ Test success valid coordinates """
        valid_coordinates = [-58.3772300, -34.6131500]

        assert validate_coordinates(valid_coordinates)

    #
    #   Wrong Tests
    #

    def test_wrong_none_coordinates(self):
        """ Test wrong none coordinates """
        self.assertRaises(ValidationError, validate_coordinates, None)

    def test_wrong_length_coordinates(self):
        """ Test wrong length coordinates """
        self.assertRaises(ValidationError, validate_coordinates, [-58.3772300, -34.6131500, 0])
        self.assertRaises(ValidationError, validate_coordinates, [-58.3772300])
        self.assertRaises(ValidationError, validate_coordinates, [])

    def test_wrong_longitude_value_coordinates(self):
        """ Test wrong longitude value coordinates """
        self.assertRaises(ValidationError, validate_coordinates, [-181, -34.6131500])
        self.assertRaises(ValidationError, validate_coordinates, [181, -34.6131500])

    def test_wrong_latitude_value_coordinates(self):
        """ Test wrong latitude value coordinates """
        self.assertRaises(ValidationError, validate_coordinates, [-58.3772300, -91])
        self.assertRaises(ValidationError, validate_coordinates, [-58.3772300, 91])
        