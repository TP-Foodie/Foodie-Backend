import pytest
from mongoengine import DoesNotExist, ValidationError

from models import User
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

    def test_average_for_calculates_average_rating_for_user(self, a_user_rating_factory, a_customer_user):
        a_user_rating_factory(rating=1)
        a_user_rating_factory(rating=1)

        assert self.user_rating_service.average_for(a_customer_user.id) == 1

    def test_average_for_works_with_floats(self, a_user_rating_factory, a_customer_user):
        a_user_rating_factory(rating=1)
        a_user_rating_factory(rating=2)

        assert self.user_rating_service.average_for(a_customer_user.id) == 1.5

    def test_creating_user_rating_should_update_user_reputation(self, a_customer_user):
        self.user_rating_service.create({
            'user': a_customer_user.id,
            'description': 'nice experience',
            'rating': 3}
        )

        assert User.objects.get(id=a_customer_user.id).reputation == 3

    def test_create_rating_with_non_existing_user_raises_error(self, an_object_id):
        with pytest.raises(DoesNotExist):
            self.user_rating_service.create({
                'user': an_object_id,
                'description': 'nice experience',
                'rating': 3}
            )

    def test_create_rating_with_wrong_number_should_raise_error(self, an_object_id):
        with pytest.raises(ValidationError):
            self.user_rating_service.create({
                'user': an_object_id,
                'description': 'nice experience',
                'rating': -1}
            )
