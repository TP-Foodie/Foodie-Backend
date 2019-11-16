from datetime import datetime, timedelta
import jwt
from settings import Config


def encode_data_to_jwt(data):
    exp_date = datetime.utcnow() + timedelta(days=90)
    data['exp'] = exp_date
    return jwt.encode(
        data,
        Config.JWT_SECRET,
        algorithm='HS256').decode('utf-8')


def decode_jwt_data(token):
    return jwt.decode(token, Config.JWT_SECRET, algorithm='HS256')
