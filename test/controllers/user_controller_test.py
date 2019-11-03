from models import User
from test.support.utils import assert_401, TestMixin, assert_200


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
