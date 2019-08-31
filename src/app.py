from flask import Flask
from flask import jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello World!"


@app.route('/places')
def places():
    places_list = [
        {
            "id": "1",
            "name": "Mac",
            "coordinates": {
                "latitude": 1,
                "longitude": 2
            }
        },
        {
            "id": "2",
            "name": "Burger",
            "coordinates": {
                "latitude": 1,
                "longitude": 2
            }
        }
    ]

    return jsonify(places_list)


@app.route('/users')
def users():
    users_list = [
        {
            "id": "1",
            "name": "Pepe Argento"
        },
        {
            "id": "2",
            "name": "Moni Potrelli"
        }
    ]

    return jsonify(users_list)


if __name__ == '__main__':
    app.run()
