from models import User


def get_users(page, limit):
    return [user for user in User.objects.skip(page * limit).limit(limit)]  # pylint: disable=E1101


def get_user(_id):
    return User.objects.get(id=_id)  # pylint: disable=E1101


def create_user(user_data):
    user = User()

    for key in user_data.keys():
        user[key] = user_data[key]

    return user.save()


def update_user(_id, user_data):
    user = get_user(_id)

    for key in user_data.keys():
        user[key] = user_data[key]

    return user.save()
