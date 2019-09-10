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