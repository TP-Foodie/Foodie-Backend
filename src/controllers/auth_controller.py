from flask import Blueprint, request, jsonify

from controllers.utils import HTTP_200_OK, HTTP_202_ACCEPTED
from schemas.authorization_schema import AuthorizationSchema, GoogleAuthorizationSchema,\
    RecoveryTokenSchema

from services import auth_service, user_service, jwt_service

AUTH_BLUEPRINT = Blueprint('auth', __name__)


@AUTH_BLUEPRINT.route('/', methods=['POST'])
def post():
    content = request.get_json()
    schema = AuthorizationSchema()
    auth_data = schema.load(content)

    data = auth_service.validate_user(auth_data)

    return jsonify({
        'token': jwt_service.encode_data_to_jwt(data),
        'id': user_service.get_user_by_email(auth_data['email']).id
    }), HTTP_200_OK


@AUTH_BLUEPRINT.route('/google', methods=['POST'])
def google_post():
    content = request.get_json()
    schema = GoogleAuthorizationSchema()
    auth_data = schema.load(content)

    data = auth_service.validate_google_user(auth_data)
    email = data['email']

    return jsonify({
        'token': jwt_service.encode_data_to_jwt(data),
        'id': user_service.get_user_by_email(email).id
    }), HTTP_200_OK


@AUTH_BLUEPRINT.route('/recovery_token', methods=['POST'])
def post_recovery_token():
    content = request.get_json()
    schema = RecoveryTokenSchema()
    recovery_data = schema.load(content)

    auth_service.generate_and_send_token(recovery_data)

    return "Ok", HTTP_202_ACCEPTED


@AUTH_BLUEPRINT.route('/password', methods=['POST'])
def post_update_password():
    # content = request.get_json()
    # schema = UpdatePasswordSchema()
    # update_password_data = schema.load(content)

    auth_service.update_password()

    return "Ok", HTTP_200_OK
