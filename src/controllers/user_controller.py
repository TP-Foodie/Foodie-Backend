from flask import jsonify
from flask import Blueprint
from flask import request

from schemas import UserSchema, UpdateUserSchema
from services import user_service

USERS_BLUEPRINT = Blueprint('users', __name__)


@USERS_BLUEPRINT.route('/<_id>', methods=['GET'])
def get_user(_id):
    return jsonify(user_service.get_user(_id)), 200


@USERS_BLUEPRINT.route('/', methods=['GET'])
def get_all():
    return jsonify(user_service.get_all_users()), 200


@USERS_BLUEPRINT.route('/', methods=['PUT'])
def patch():
    content = request.get_json()
    schema = UpdateUserSchema()
    user_data = schema.load(content)

    return jsonify(user_service.update_user(user_data))


@USERS_BLUEPRINT.route('/', methods=['POST'])
def post():
    content = request.get_json()
    schema = UserSchema()
    user_data = schema.load(content)

    return jsonify(user_service.save_user(user_data)), 201
