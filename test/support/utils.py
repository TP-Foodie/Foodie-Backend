import json

from controllers.utils import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, \
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


class TestMixin:
    def login(self, client, email, password):
        response = client.post(
            '/api/v1/auth/',
            json={'email': email, 'password': password}
        )
        self.token = json.loads(response.data)['token']
        return self.token

    def get(self, client, url):
        return client.get(
            url,
            headers={'Authorization': 'Bearer {}'.format(self.token)}
        )

    def post(self, client, url, data):
        return client.post(
            url,
            json=data,
            headers={'Authorization': 'Bearer {}'.format(self.token)}
        )
