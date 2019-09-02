from flask import Flask
from flask import jsonify
from models.user import User
from models.place import Place, Coordinates
from encoders import CustomJSONEncoder
from pymongo import MongoClient

APP = Flask(__name__)

client = MongoClient('localhost:27017',
              username='app',
              password='password',
              authSource='foodie',
              authMechanism='SCRAM-SHA-1')


@APP.route('/places')
def places():
    places_list = [
        Place("1", "Mac", Coordinates(1.0, 2.0)),
        Place("1", "Burger", Coordinates(1.0, 2.0)),
    ]

    return jsonify(places_list)


@APP.route('/users')
def users():
    user = client.foodie.users.find_one()
    return jsonify({
        "id": user["_id"]._pid,
        "name": user["name"]
    })

if __name__ == '__main__':
    APP.json_encoder = CustomJSONEncoder
    APP.run()
