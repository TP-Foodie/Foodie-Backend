from flask import Flask
from flask import jsonify
from models.user import User
from models.place import Place, Coordinates
from encoders import CustomJSONEncoder

APP = Flask(__name__)


@APP.route('/places')
def places():
    places_list = [
        Place("1", "Mac", Coordinates(1.0, 2.0)),
        Place("1", "Burger", Coordinates(1.0, 2.0)),
    ]

    return jsonify(places_list)


@APP.route('/users')
def users():
    users_list = [
        User("1", "Pepe Argento"),
        User("2", "Moni Potrelli")
    ]

    return jsonify(users_list)


if __name__ == '__main__':
    APP.json_encoder = CustomJSONEncoder
    APP.run()
