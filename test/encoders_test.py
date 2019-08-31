from encoders import CustomJSONEncoder
from models import user, place


def test_user_json_encode():
    encoder = CustomJSONEncoder()

    expected = {
        "id": "1",
        "name": "Pepe Argento"
    }

    assert expected == encoder.default(user.User("1", "Pepe Argento"))


def test_place_json_encode():
    encoder = CustomJSONEncoder()

    expected = {
        "id": "1",
        "name": "Mac",
        "coordinates": {
            "latitude": 1.0,
            "longitude": 1.0
        }
    }

    assert expected == encoder.default(place.Place("1", "Mac", place.Coordinates(1.0, 1.0)))
