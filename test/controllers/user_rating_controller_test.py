from test.support.utils import TestMixin, assert_401


class TestUserRatingController(TestMixin):
    def test_create_for_unauthenticated(self, a_client, a_user_rating):
        response = a_client.post('api/v1/user_ratings/', json=a_user_rating.to_json())

        assert_401(response)
