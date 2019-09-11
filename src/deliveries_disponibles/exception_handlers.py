""" This Module handles exceptions thrown in deliveries disponibles endpoint """

from flask import jsonify, Blueprint

from deliveries_disponibles.services.deliveries_disponibles_service import COLLECTION_DELIVERIES_DISPONIBLES
from deliveries_disponibles.exceptions import DeliveryYaDisponibleException, DeliveryNoDisponibleException, ValidationException

# blueprints Flask
DELIVERIES_DISPONIBLES_EXCEPTIONS_HANDLER = \
    Blueprint('deliveries_disponibles_exception_handlers', __name__)

@DELIVERIES_DISPONIBLES_EXCEPTIONS_HANDLER.app_errorhandler(DeliveryYaDisponibleException)
def delivery_ya_disponible_handler(error):
    """ This Method handles exception: delivery ya disponible en la db """
    return jsonify({"error": error.msg}), 400

@DELIVERIES_DISPONIBLES_EXCEPTIONS_HANDLER.app_errorhandler(DeliveryNoDisponibleException)
def delivery_no_disponible_handler(error):
    """ This Method handles exception: delivery no disponible en la db """
    return jsonify({"error": error.msg}), 400

@DELIVERIES_DISPONIBLES_EXCEPTIONS_HANDLER.app_errorhandler(ValidationException)
def validation_error_handler(error):
    """ This Method handles exception: error de validacion en los datos recibidos
    a traves de la api """
    return jsonify({"error": error.msg}), 400
