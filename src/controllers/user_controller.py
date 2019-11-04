from flask import jsonify
from flask import Blueprint
from flask import request

from schemas.user import CreateUserSchema, UpdateUserSchema
from services import user_service
from services.auth_service import authenticate
from models.user_profile import UserProfile

USERS_BLUEPRINT = Blueprint('users', __name__)


@USERS_BLUEPRINT.route('/me', methods=['GET'])
@authenticate
def get_me(user):
    return jsonify(user), 200


@USERS_BLUEPRINT.route('/<_id>', methods=['GET'])
def get_user(_id):
    user = user_service.get_user(_id)
    user_profile = UserProfile(
        user.name, user.last_name, user.email, user.profile_image,
        user.type, user.subscription, user.reputation, user.messages_sent
    )
    return jsonify(user_profile), 200


@USERS_BLUEPRINT.route('/', methods=['GET'])
def get_users():
    page = int(request.args.get("page", 0))
    limit = int(request.args.get("limit", 50))

    return jsonify(
        {
            "page": page,
            "limit": limit,
            "users": user_service.get_users(page, limit)
        }
    ), 200


@USERS_BLUEPRINT.route('/me', methods=['PATCH'])
@authenticate
def patch_me(user):
    return patch(user.id)


@USERS_BLUEPRINT.route('/<_id>', methods=['PATCH'])
@authenticate
def patch(_id):
    content = request.get_json()
    schema = UpdateUserSchema()
    user_data = schema.load(content)

    return jsonify(user_service.update_user(_id, user_data))


@USERS_BLUEPRINT.route('/', methods=['POST'])
def post():
    content = request.get_json()
    schema = CreateUserSchema()
    user_data = schema.load(content)

    return jsonify(user_service.create_user(user_data)), 201
