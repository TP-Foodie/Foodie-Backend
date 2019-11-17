import json

from models.user_rating import UserRating
from test.support.utils import TestMixin, assert_401, assert_201


class TestUserRatingController(TestMixin):
    def test_create_for_unauthenticated(self, a_client, a_user_rating):
        response = a_client.post('api/v1/user_ratings/', json=a_user_rating.to_json())

        assert_401(response)

    def test_create_user_rating(self, a_client, a_client_user, a_user_rating):
        self.login(a_client, a_client_user.email, a_client_user.password)

        response = self.post(
            a_client,
            'api/v1/user_ratings/',
            json.dumps({
                'user': str(a_user_rating.user.id),
                'rating': 5
            })
        )

        assert_201(response)

        assert UserRating.objects.count() == 2

    def test_create_user_rating_should_return_it(self, a_client, a_client_user, a_user_rating):
        self.login(a_client, a_client_user.email, a_client_user.password)

        response = self.post(
            a_client,
            'api/v1/user_ratings/',
            json.dumps({
                'user': str(a_user_rating.user.id),
                'rating': 5
            })
        )

        user_rating = json.loads(response.data)

        assert user_rating == {
            'id': str(user_rating['id']),
            'user': {'id': str(a_user_rating.user.id)},
            'description': None,
            'rating': 5
        }
