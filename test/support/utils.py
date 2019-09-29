from src.controllers.utils import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST,\
    HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED


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


def assert_404(response):
    assert response.status_code == HTTP_404_NOT_FOUND


def assert_401(response):
    assert response.status_code == HTTP_401_UNAUTHORIZED
