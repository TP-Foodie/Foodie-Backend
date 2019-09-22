from src.models import User


def delivery_exists(delivery_id):
    return User.objects.filter(type=User.DELIVERY_TYPE, id=delivery_id).count() > 0
