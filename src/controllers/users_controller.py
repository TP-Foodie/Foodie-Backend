from src.repositories.mongo_client import client
from flask import jsonify
from flask import Blueprint
from flask import request

users_blueprint = Blueprint('users', __name__)


@users_blueprint.route('/', methods=['GET'])
def get():
    users = client.foodie.users.find()
    response = {}

    response["users"] = [{
        "id": user["_id"],
        "name": user["name"]
    } for user in users]

    return jsonify(response)


@users_blueprint.route('/', methods=['POST'])
def post():
    name = request.json['name']
    client.foodie.users.insert_one({'name': name})
    return "ok"

