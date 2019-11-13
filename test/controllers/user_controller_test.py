import json

from test.support.utils import assert_401, TestMixin, assert_200
from models import User


class TestUserController(TestMixin):
    def test_update_for_unauthenticated(self, a_client, a_customer_user):
        response = a_client.patch('api/v1/users/{}'.format(str(a_customer_user.id)))

        assert_401(response)

    def test_update_user_location(self, a_client, a_client_user, a_location):
        self.login(a_client, a_client_user.email, a_client_user.password)
        response = self.patch(
            a_client,
            '/api/v1/users/{}'.format(a_client_user.id),
            {'location': a_location}
        )

        assert_200(response)
        assert User.objects.get(id=a_client_user.id).location == a_location

    def test_update_user_balance(self, a_client, a_client_user):
        self.login(a_client, a_client_user.email, a_client_user.password)
        response = self.patch(
            a_client,
            '/api/v1/users/{}'.format(a_client_user.id),
            {'balance': 10}
        )

        assert_200(response)
        assert User.objects.get(id=a_client_user.id).balance == 10

    def test_get_me_for_unauthenticated(self, a_client):
        response = a_client.get('api/v1/users/me')
        assert_401(response)

    def test_get_me(self, a_client, a_client_user):
        self.login(a_client, a_client_user.email, a_client_user.password)
        response = self.get(a_client, 'api/v1/users/me')

        assert_200(response)
        user_data = json.loads(response.data)
        assert user_data["id"] == str(a_client_user.id)
        assert user_data["name"] == a_client_user.name
        assert user_data["email"] == a_client_user.email
        assert user_data["type"] == a_client_user.type

    def test_get_me_admin(self, a_client, an_admin_user):
        self.login(a_client, an_admin_user.email, an_admin_user.password)
        response = self.get(a_client, 'api/v1/users/me')

        assert_200(response)
        user_data = json.loads(response.data)
        assert user_data["id"] == str(an_admin_user.id)
        assert user_data["name"] == an_admin_user.name
        assert user_data["email"] == an_admin_user.email
        assert user_data["type"] == an_admin_user.type

    def test_get_users_from_customer(self, a_client, a_client_user):
        self.login(a_client, a_client_user.email, a_client_user.password)
        response = self.get_paging(a_client, 'api/v1/users/', 0, 50)
        assert_401(response)

    def test_get_users_from_admin_user(self, a_client, an_admin_user):
        self.login(a_client, an_admin_user.email, an_admin_user.password)
        response = self.get_paging(a_client, 'api/v1/users/', 0, 50)
        assert an_admin_user.type == "BACK_OFFICE"
        assert_200(response)

    def test_get_complete_user_data_when_admin_user(self, a_client, an_admin_user, a_customer_user):
        self.login(a_client, an_admin_user.email, an_admin_user.password)
        response = self.get(a_client, 'api/v1/users/{}'.format(str(a_customer_user.id)))
        assert_200(response)

        customer_data = json.loads(response.data)
        assert a_customer_user
        assert "phone" in customer_data

    def test_get_public_user_data_when_customer_user(
            self, a_client, a_client_user, a_customer_user
    ):
        self.login(a_client, a_client_user.email, a_client_user.password)
        response = self.get(a_client, 'api/v1/users/{}'.format(str(a_customer_user.id)))
        assert_200(response)

        customer_data = json.loads(response.data)
        assert a_customer_user.name == customer_data["name"]
