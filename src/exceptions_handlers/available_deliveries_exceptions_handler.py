""" This Module handles exceptions thrown in available deliveries endpoint """

from flask import jsonify, Blueprint

from my_exceptions.available_deliveries_exceptions import (
    DeliveryAlreadyAvailableException, DeliveryNotAvailableException, ValidationException)

# blueprints Flask
AVAILABLE_DELIVERIES_EXCEPTIONS_HANDLER = \
    Blueprint('available_deliveries_exception_handlers', __name__)

@AVAILABLE_DELIVERIES_EXCEPTIONS_HANDLER.app_errorhandler(DeliveryAlreadyAvailableException)
def delivery_already_available_handler(error):
    """ This Method handles exception: delivery already available in db. """
    return jsonify({"error": error.msg}), 400

@AVAILABLE_DELIVERIES_EXCEPTIONS_HANDLER.app_errorhandler(DeliveryNotAvailableException)
def delivery_not_available_handler(error):
    """ This Method handles exception: delivery not available in db. """
    return jsonify({"error": error.msg}), 400

@AVAILABLE_DELIVERIES_EXCEPTIONS_HANDLER.app_errorhandler(ValidationException)
def request_data_validation_error_handler(error):
    """ This Method handles exception: validation error of request data. """
    return jsonify({"error": error.msg}), 400
