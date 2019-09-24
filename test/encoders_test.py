import datetime
from unittest.mock import create_autospec
from mongoengine import Document

from src.encoders import CustomJSONEncoder

ENCODER = CustomJSONEncoder()


class TestEncoder:

    def test_datetime_json_encode(self):
        """
        Test to ensure that the default behaviour is still valid
        """

        expected = '"Sat, 31 Aug 2019 20:58:53 GMT"'
        date = datetime.datetime(2019, 8, 31, 20, 58, 53, 391516)

        assert expected == ENCODER.encode(date)

    def test_mongo_document(self):
        """
        Test to ensure mongo document model works
        """
        expected = {"name": "jose"}
        document = create_autospec(Document)

        document._data = {"name": "jose"}  # pylint: disable=W0212

        assert ENCODER.encode(expected) == ENCODER.encode(document)
