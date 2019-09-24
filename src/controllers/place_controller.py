from flask import jsonify
from flask import Blueprint

from models import Place

PLACES_BLUEPRINT = Blueprint('places', __name__)


@PLACES_BLUEPRINT.route('/', methods=['GET'])
def get():
    return jsonify([place for place in Place.objects])  # pylint: disable=E1101
