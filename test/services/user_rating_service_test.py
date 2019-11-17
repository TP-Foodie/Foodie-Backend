import pytest

from models.user_rating import UserRating
from services.user_rating_service import UserRatingService


@pytest.mark.usefixtures('a_client')
class TestUserRating:
    user_rating_service = UserRatingService()

    def test_create_should_create_one(self, a_customer_user):
        self.user_rating_service.create({
            'user': a_customer_user.id,
            'description': 'nice experience',
            'rating': 1}
        )

        assert UserRating.objects.count() == 1
