from functools import wraps
from flask import request
from google.oauth2 import id_token
from google.auth.transport import requests
from mongoengine import DoesNotExist

from services import user_service, jwt_service
from services.exceptions.unauthorized_user import UnauthorizedUserException
from settings import Config


def validate_user(auth_data):
    if user_service.is_valid(auth_data['email'], auth_data['password']):
        return auth_data
    raise UnauthorizedUserException()


def authenticate(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        auth = request.headers['Authorization']
        way = ''
        token = ''

        try:
            way, token = auth.split()
        except ValueError:
            pass

        if way != "Bearer":
            raise UnauthorizedUserException

        auth_data = jwt_service.decode_jwt_data(token)

        if 'sub' in auth_data:
            user_is_valid = user_service.is_valid(google_id=auth_data['sub'])
        else:
            user_is_valid = user_service.is_valid(
                email=auth_data['email'],
                password=auth_data['password'])

        if not user_is_valid:
            raise UnauthorizedUserException

        return function(*args, **kwargs)

    return wrapper


def validate_google_user(auth_data):
    id_info = id_token \
        .verify_oauth2_token(
            auth_data['google_token'],
            requests.Request(),
            Config.GOOGLE_CLIENT_ID)

    if id_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
        raise UnauthorizedUserException

    try:
        user_service.get_user_by_email(id_info['email'])
    except DoesNotExist:
        user_service.create_user_from_google_data(id_info)

    return id_info
