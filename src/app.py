from flask import Flask
from flask import jsonify
from models.User import User
from models.Place import Place, Coordinates
from encoders import CustomJSONEncoder

app = Flask(__name__)


@app.route('/places')
def places():
    places_list = [
        Place("1", "Mac", Coordinates(1.0, 2.0)),
        Place("1", "Burger", Coordinates(1.0, 2.0)),
    ]

    return jsonify(places_list)


@app.route('/users')
def users():
    users_list = [
        User("1", "Pepe Argento"),
        User("2", "Moni Potrelli")
    ]

    return jsonify(users_list)


if __name__ == '__main__':
    app.json_encoder = CustomJSONEncoder
    app.run()
