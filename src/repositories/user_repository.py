from models import User


def delivery_exists(delivery_id):
    return User.objects.filter(type=User.DELIVERY_TYPE, id=delivery_id).count() > 0


def get_user(id_user):
    return User.objects.get(id=id_user)


def increment_messages_sent(id_user):
    User.objects(id=id_user).update_one(inc__messages_sent=1)
