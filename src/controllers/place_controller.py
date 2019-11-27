from flask import jsonify
from flask import Blueprint

from logger import log_request_response
from models.place import Place

PLACES_BLUEPRINT = Blueprint('places', __name__)


@PLACES_BLUEPRINT.route('/', methods=['GET'])
@log_request_response
def get():
    return jsonify([place for place in Place.objects])  # pylint: disable=E1101
