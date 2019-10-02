from flask import Blueprint, request, jsonify

from controllers.utils import HTTP_200_OK
from schemas.authorization_schema import AuthorizationSchema, GoogleAuthorizationSchema

from services import auth_service, user_service

AUTH_BLUEPRINT = Blueprint('auth', __name__)


@AUTH_BLUEPRINT.route('/', methods=['POST'])
def post():
    content = request.get_json()
    schema = AuthorizationSchema()
    auth_data = schema.load(content)

    return jsonify({
        'token': auth_service.validate_user(auth_data),
        'id': user_service.get_user_by_email(auth_data['email'])
    }), HTTP_200_OK


@AUTH_BLUEPRINT.route('/google', methods=['POST'])
def google_post():
    content = request.get_json()
    schema = GoogleAuthorizationSchema()
    auth_data = schema.load(content)

    return jsonify({
        'token': auth_service.validate_google_user(auth_data),
        'id': user_service.get_user_by_email(auth_data['email'])
    }), HTTP_200_OK
