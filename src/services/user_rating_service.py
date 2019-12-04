from models.user_rating import UserRating
from repositories.user_rating_repository import UserRatingRepository
from services import user_service, order_service


class UserRatingService:
    user_rating_repository = UserRatingRepository()

    def create(self, data):
        rating = UserRating(**data).save()

        user_service.update_user({'reputation': self.average_for(rating.user)}, rating.user.id)

        delivery_id = rating.order.delivery.id
        if delivery_id == rating.user.id:
            order_service.update(rating.order.id, {"delivery_rated": True})
        else:
            order_service.update(rating.order.id, {"owner_rated": True})

        return rating

    def average_for(self, user_id):
        ratings = self.user_rating_repository.filter(user=user_id).values_list('rating')
        return sum(ratings) / len(ratings)
