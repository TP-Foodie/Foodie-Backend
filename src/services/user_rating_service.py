from models.user_rating import UserRating


class UserRatingService:
    def create(self, data):
        UserRating(**data).save()
