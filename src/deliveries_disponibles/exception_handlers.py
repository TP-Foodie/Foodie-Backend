from flask import jsonify, Blueprint

from deliveries_disponibles.services.deliveries_disponibles_service import COLLECTION_DELIVERIES_DISPONIBLES
from deliveries_disponibles.exceptions import DeliveryYaDisponibleException, DeliveryNoDisponibleException, ValidationException

# blueprints Flask
deliveries_disponibles_exception_handlers_blueprint = Blueprint('deliveries_disponibles_exception_handlers', __name__)

@deliveries_disponibles_exception_handlers_blueprint.app_errorhandler(DeliveryYaDisponibleException)
def delivery_ya_disponible_handler(e):
    return jsonify({"error": e.msg}), 400

@deliveries_disponibles_exception_handlers_blueprint.app_errorhandler(DeliveryNoDisponibleException)
def delivery_no_disponible_handler(e):
    return jsonify({"error": e.msg}), 400

@deliveries_disponibles_exception_handlers_blueprint.app_errorhandler(ValidationException)
def validation_error_handler(e):
    return jsonify({"error": e.msg}), 400