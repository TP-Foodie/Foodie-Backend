import hashlib

from models import User


def get_users(page, limit):
    return [user for user in User.objects.skip(
        page * limit).limit(limit)]  # pylint: disable=E1101


def get_user(_id):
    return User.objects.get(id=_id)  # pylint: disable=E1101


def get_user_by_user_name(user_name):
    return User.objects.get(user_name=user_name)


def create_user(user_data):
    user = User()

    for key in user_data.keys():
        user[key] = _get_property(user_data, key)

    return user.save()


def update_user(_id, user_data):
    user = get_user_by_id(_id)

    for key in user_data.keys():
        user[key] = _get_property(user_data, key)

    return user.save()


def is_valid(user_name, password):
    return get_user_by_user_name(
        user_name).password == _hash_password(password)


def _hash_password(password):
    return hashlib.md5(password.encode('utf-8')).hexdigest()


def _get_property(data, key):
    if key == 'password':
        return _hash_password(data[key])

    return data[key]
