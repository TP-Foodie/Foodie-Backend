from bson import ObjectId
from flask import jsonify
from flask import Blueprint
from flask import request

from schemas import user_schemas
from models.user import User

USERS_BLUEPRINT = Blueprint('users', __name__)


@USERS_BLUEPRINT.route('/<_id>', methods=['GET'])
def get_user(_id):
    user = User.objects.get(id=_id)
    return jsonify(user)


@USERS_BLUEPRINT.route('/', methods=['GET'])
def get():
    return jsonify([user for user in User.objects])


@USERS_BLUEPRINT.route('/', methods=['POST'])
def post():
    content = request.get_json()
    schema = user_schemas.UserSchema()
    user_data = schema.load(content)

    user = User()
    for key in schema.declared_fields.keys():
        user[key] = user_data[key]

    return jsonify(user.save())
