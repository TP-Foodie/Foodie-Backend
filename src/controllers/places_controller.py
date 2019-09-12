from flask import jsonify
from flask import Blueprint

from models.place import Place, Coordinates

PLACES_BLUEPRINT = Blueprint('places', __name__)


@PLACES_BLUEPRINT.route('/')
def get():
    places_list = [
        Place("1", "Mac", Coordinates(1.0, 2.0)),
        Place("1", "Burger", Coordinates(1.0, 2.0)),
    ]

    return jsonify(places_list)
