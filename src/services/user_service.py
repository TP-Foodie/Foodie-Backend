import hashlib

from models import User


def get_users(page, limit):
    return [user for user in User.objects.skip(
        page * limit).limit(limit)]  # pylint: disable=E1101


def get_user(_id):
    return User.objects.get(id=_id)  # pylint: disable=E1101


def get_user_by_google_id(google_id):
    return User.objects.get(google_id=google_id)


def get_user_by_email(email):
    return User.objects.get(email=email)


def create_user(user_data):
    user = User()

    for key in user_data.keys():
        user[key] = _get_property(user_data, key)

    return user.save()


def update_user(_id, user_data):
    user = get_user(_id)

    for key in user_data.keys():
        user[key] = _get_property(user_data, key)

    return user.save()


def is_valid(email=None, password=None, google_id=None):
    if google_id is not None:
        user = get_user_by_google_id(google_id)
        return user is not None

    user = get_user_by_email(email)

    if user is None:
        return False

    return user.password == _hash_password(password)


def _hash_password(password):
    return hashlib.md5(password.encode('utf-8')).hexdigest()


def _get_property(data, key):
    if key == 'password':
        return _hash_password(data[key])

    return data[key]


def create_user_from_google_data(google_data):
    user_data = {
        'name': google_data['given_name'],
        'last_name': google_data['family_name'],
        'google_id': google_data['sub'],
        'email': google_data['email'],
        'profile_image': google_data['picture'],
    }

    create_user(user_data)
