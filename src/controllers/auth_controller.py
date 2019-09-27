from flask import Blueprint, request, jsonify

from controllers.utils import HTTP_200_OK
from schemas.authorization_schema import AuthorizationSchema

from services import auth_service

AUTH_BLUEPRINT = Blueprint('auth', __name__)


@AUTH_BLUEPRINT.route('/', methods=['POST'])
def post():
    content = request.get_json()
    schema = AuthorizationSchema()
    auth_data = schema.load(content)

    return jsonify({
        'token': auth_service.validate_user(auth_data)
    }), HTTP_200_OK
