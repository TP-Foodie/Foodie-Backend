from flask import Blueprint, request, jsonify

from controllers.utils import HTTP_200_OK, HTTP_202_ACCEPTED
from logger import log_request_response
from schemas.authorization_schema import AuthorizationSchema, GoogleAuthorizationSchema, \
    RecoveryTokenSchema, UpdatePasswordSchema

from services import auth_service, jwt_service

AUTH_BLUEPRINT = Blueprint('auth', __name__)


@AUTH_BLUEPRINT.route('/', methods=['POST'])
@log_request_response
def post():
    content = request.get_json()
    schema = AuthorizationSchema()
    auth_data = schema.load(content)

    data = auth_service.validate_user(auth_data)

    return jsonify({
        'token': jwt_service.encode_data_to_jwt(data)
    }), HTTP_200_OK


@AUTH_BLUEPRINT.route('/google', methods=['POST'])
@log_request_response
def google_post():
    content = request.get_json()
    schema = GoogleAuthorizationSchema()
    auth_data = schema.load(content)

    data = auth_service.validate_google_user(auth_data)

    return jsonify({
        'token': jwt_service.encode_data_to_jwt(data)
    }), HTTP_200_OK


@AUTH_BLUEPRINT.route('/recovery_token', methods=['POST'])
@log_request_response
def post_recovery_token():
    content = request.get_json()
    schema = RecoveryTokenSchema()
    recovery_data = schema.load(content)

    auth_service.generate_and_send_token(recovery_data)

    return jsonify({'status': 'ok'}), HTTP_202_ACCEPTED


@AUTH_BLUEPRINT.route('/password', methods=['POST'])
@log_request_response
def post_update_password():
    content = request.get_json()
    schema = UpdatePasswordSchema()
    update_password_data = schema.load(content)

    auth_service.update_password(update_password_data)

    return jsonify({'status': 'ok'}), HTTP_200_OK
