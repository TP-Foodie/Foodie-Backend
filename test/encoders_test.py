from encoders import CustomJSONEncoder
from models import user, place
import datetime

encoder = CustomJSONEncoder()


def test_datetime_json_encode():
    """
    Test to ensure that the default behaviour is still valid
    """

    expected = '"Sat, 31 Aug 2019 20:58:53 GMT"'
    d = datetime.datetime(2019, 8, 31, 20, 58, 53, 391516)

    assert expected == encoder.encode(d)


def test_user_json_encode():
    expected = {
        "id": "1",
        "name": "Pepe Argento"
    }

    assert expected == encoder.default(user.User("1", "Pepe Argento"))


def test_place_json_encode():
    expected = {
        "_id": "1",
        "name": "Mac",
        "coordinates": {
            "latitude": 1.0,
            "longitude": 1.0
        }
    }

    assert expected == encoder.default(place.Place("1", "Mac", place.Coordinates(1.0, 1.0)))
