from unittest.mock import Mock, create_autospec

from mongoengine import Document

from encoders import CustomJSONEncoder
import datetime

encoder = CustomJSONEncoder()


def test_datetime_json_encode():
    """
    Test to ensure that the default behaviour is still valid
    """

    expected = '"Sat, 31 Aug 2019 20:58:53 GMT"'
    d = datetime.datetime(2019, 8, 31, 20, 58, 53, 391516)

    assert expected == encoder.encode(d)


def test_mongo_document():
    """
    Test to ensure mongo document model works
    """
    expected = {"name": "jose"}
    document = create_autospec(Document)

    document._data = {"name": "jose"}

    assert encoder.encode(expected) == encoder.encode(document)
