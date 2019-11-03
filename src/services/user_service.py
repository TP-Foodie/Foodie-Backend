import random
from datetime import datetime, timedelta
import hashlib

from models import User
from services.exceptions.unauthorized_user import UnauthorizedUserException


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

    data = user_data
    if 'password' in user_data:
        data['password'] = _get_property(user_data, 'password')

    user.update(**data)


def is_valid(email=None, password=None, google_id=None, user=None):

    if google_id is not None:
        user = get_user_by_google_id(google_id)
        return user is not None

    if email is not None:
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


def set_recovery_token(email):
    recovery_token = _get_random_number()
    user = get_user_by_email(email)
    user.recovery_token = recovery_token
    user.recovery_token_date = datetime.utcnow()
    user.save()
    return recovery_token


def _get_random_number():
    return str(round(random.random() * 10000))


def verify_user_token(update_password_data):
    user = get_user_by_email(update_password_data['email'])

    if user.recovery_token != update_password_data['recovery_token']:
        raise UnauthorizedUserException

    if user.recovery_token_date + timedelta(days=1) < datetime.utcnow():
        raise UnauthorizedUserException


def update_user_password(update_password_data):
    user = get_user_by_email(update_password_data['email'])
    user.password = _hash_password(update_password_data['password'])
    user.save()
