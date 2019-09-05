from flask import jsonify
from models.place import Place, Coordinates
from flask import Blueprint

places_blueprint = Blueprint('places', __name__)


@places_blueprint.route('/')
def get():
    places_list = [
        Place("1", "Mac", Coordinates(1.0, 2.0)),
        Place("1", "Burger", Coordinates(1.0, 2.0)),
    ]

    return jsonify(places_list)
