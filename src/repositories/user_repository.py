from models import User


def delivery_exists(delivery_id, is_favour):
    if (is_favour):
        return User.objects.filter(type=User.CUSTOMER_TYPE, id=delivery_id).count() > 0
    return User.objects.filter(type=User.DELIVERY_TYPE, id=delivery_id).count() > 0


def get_user(id_user):
    return User.objects.get(id=id_user)


def increment_messages_sent(id_user):
    User.objects(id=id_user).update_one(inc__messages_sent=1)


def increment_deliveries_completed(id_user):
    User.objects(id=id_user).update_one(inc__deliveries_completed=1)


def set_delivery_as_unavailable(delivery_id):
    get_user(delivery_id).update(available=False)


def set_delivery_as_available(delivery_id):
    get_user(delivery_id).update(available=True)


def get_nearby_available_deliveries(longitude, latitude, radius):
    return User.objects(  # pylint: disable=E1101
        location__geo_within_center=[[longitude, latitude], radius],
        type=User.DELIVERY_TYPE,
        available=True
    )


def update(user_id, data):
    return get_user(user_id).update(**data)
