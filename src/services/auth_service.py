from functools import wraps

from flask import request

from services import user_service, jwt_service
from services.exceptions.unauthorized_user import UnauthorizedUserException


def validate_user(auth_data):
    if user_service.is_valid(auth_data['email'], auth_data['password']):
        return jwt_service.encode_data_to_jwt(auth_data)
    raise UnauthorizedUserException()


def authenticate(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        auth = request.headers.get('Authorization', '')
        way = ''
        token = ''

        try:
            way, token = auth.split()
        except ValueError:
            pass

        if way != "Bearer":
            raise UnauthorizedUserException

        auth_data = jwt_service.decode_jwt_data(token)
        user_is_valid = user_service.is_valid(auth_data['email'], auth_data['password'])

        if not user_is_valid:
            raise UnauthorizedUserException

        return function(*args, **kwargs)

    return wrapper
