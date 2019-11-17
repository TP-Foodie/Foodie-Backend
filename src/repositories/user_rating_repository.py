from models.user_rating import UserRating


class UserRatingRepository:
    def filter(self, **filter_values):
        return UserRating.objects.filter(**filter_values)
