import jwt
from settings import Config


def encode_data_to_jwt(data):
    return jwt.encode(
        data,
        Config.JWT_SECRET,
        algorithm='HS256').decode('utf-8')


def decode_jwt_data(token):
    return jwt.decode(token, Config.JWT_SECRET, algorithm='HS256', audience=Config.GOOGLE_CLIENT_ID)
