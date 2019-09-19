from src.controllers.utils import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST


def assert_attr_exists(obj, attr_name):
    try:
        getattr(obj, attr_name)
        assert True
    except KeyError:
        assert False


def assert_200(response):
    assert response.status_code == HTTP_200_OK


def assert_201(response):
    assert response.status_code == HTTP_201_CREATED


def assert_400(response):
    assert response.status_code == HTTP_400_BAD_REQUEST
