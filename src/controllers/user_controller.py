from flask import jsonify
from flask import Blueprint
from flask import request

from logger import log_request_response
from schemas.user import CreateUserSchema, UpdateUserSchema, UserProfile
from services import user_service
from services.auth_service import authenticate
from models import User
from controllers.utils import HTTP_200_OK, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED

USERS_BLUEPRINT = Blueprint('users', __name__)


@USERS_BLUEPRINT.route('/me', methods=['GET'])
@log_request_response
@authenticate
def get_me(user):
    return jsonify(user), HTTP_200_OK


@USERS_BLUEPRINT.route('/<_id>', methods=['GET'])
@log_request_response
@authenticate
def get_user(user, _id):
    if user.type == User.BACK_OFFICE_TYPE:
        return jsonify(user_service.get_user(_id)), HTTP_200_OK

    user_data = user_service.get_user(_id)
    user_profile = UserProfile().dump(user_data)
    return jsonify(user_profile), HTTP_200_OK


@USERS_BLUEPRINT.route('/', methods=['GET'])
@log_request_response
@authenticate
def get_users(user):
    page = int(request.args.get("page", 0))
    limit = int(request.args.get("limit", 50))

    if user.type == User.BACK_OFFICE_TYPE:
        return jsonify({
            "page": page,
            "limit": limit,
            "users": user_service.get_users(page, limit)
        }), HTTP_200_OK

    return jsonify({}), HTTP_401_UNAUTHORIZED


@USERS_BLUEPRINT.route('/me', methods=['PATCH'])
@log_request_response
@authenticate
def patch_me(user):
    content = request.get_json()
    schema = UpdateUserSchema()
    user_data = schema.load(content)

    return jsonify(user_service.update_user(user_data, user=user))


@USERS_BLUEPRINT.route('/<_id>', methods=['PATCH'])
@log_request_response
@authenticate
def patch(_id):
    content = request.get_json()
    schema = UpdateUserSchema()
    user_data = schema.load(content)

    return jsonify(user_service.update_user(user_data, _id=_id))


@USERS_BLUEPRINT.route('/', methods=['POST'])
@log_request_response
def post():
    content = request.get_json()
    schema = CreateUserSchema()
    user_data = schema.load(content)

    return jsonify(user_service.create_user(user_data)), HTTP_201_CREATED
