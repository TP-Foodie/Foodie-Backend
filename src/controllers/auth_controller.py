from flask import Blueprint, request, jsonify

from controllers.utils import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from schemas.authorization_schema import AuthorizationSchema

from services import user_service, jwt_service

AUTH_BLUEPRINT = Blueprint('auth', __name__)


@AUTH_BLUEPRINT.route('/', methods=['POST'])
def post():
    content = request.get_json()
    schema = AuthorizationSchema()
    auth_data = schema.load(content)

    if user_service.is_valid(auth_data['email'], auth_data['password']):
        token = jwt_service.encode_data_to_jwt(auth_data)
        return jsonify({
            'token': token
        }), HTTP_200_OK

    return 'UNAUTHORIZED', HTTP_401_UNAUTHORIZED
