from models.user_rating import UserRating


class UserRatingService:
    def create(self, data):
        UserRating(**data).save()

    def average_for(self, user_id):
        return 1
