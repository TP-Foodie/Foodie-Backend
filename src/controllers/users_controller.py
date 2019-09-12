from bson import ObjectId
from flask import jsonify
from flask import Blueprint
from flask import request

from repositories.mongo_client import CLIENT
from schemas import user_schemas

USERS_BLUEPRINT = Blueprint('users', __name__)


@USERS_BLUEPRINT.route('/<_id>', methods=['GET'])
def get_user(_id):
    user = CLIENT.foodie.users.find_one({'_id': ObjectId(_id)})
    return jsonify(user)


@USERS_BLUEPRINT.route('/', methods=['GET'])
def get():
    users = CLIENT.foodie.users.find()

    return jsonify({"users": [user for user in users]})


@USERS_BLUEPRINT.route('/', methods=['POST'])
def post():
    content = request.get_json()
    schema = user_schemas.UserSchema()
    user_data = schema.load(content)

    return jsonify(
        {
            "_id": CLIENT.foodie.users.insert_one(user_data).inserted_id
        }
    )
