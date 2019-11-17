from models.user_rating import UserRating
from repositories.user_rating_repository import UserRatingRepository


class UserRatingService:
    user_rating_repository = UserRatingRepository()

    def create(self, data):
        UserRating(**data).save()

    def average_for(self, user_id):
        ratings = self.user_rating_repository.filter(user=user_id).values_list('rating')
        return sum(ratings) / len(ratings)
