from bson import ObjectId

from repositories.mongo_client import client
from flask import jsonify
from flask import Blueprint
from flask import request

from schemas import user_schemas

users_blueprint = Blueprint('users', __name__)


@users_blueprint.route('/<_id>', methods=['GET'])
def get_user(_id):
    user = client.foodie.users.find_one({'_id': ObjectId(_id)})
    return jsonify(user)


@users_blueprint.route('/', methods=['GET'])
def get():
    users = client.foodie.users.find()

    return jsonify({"users": [user for user in users]})


@users_blueprint.route('/', methods=['POST'])
def post():
    content = request.get_json()
    schema = user_schemas.UserSchema()
    user_data = schema.load(content)

    return jsonify(
        {
            "_id": client.foodie.users.insert_one(user_data).inserted_id
        }
    )
