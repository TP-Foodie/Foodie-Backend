from flask import jsonify
from marshmallow import ValidationError as MarshmallowValidationError
from mongoengine import ValidationError as MongoValidationError
from mongoengine import DoesNotExist


def marshmallow_validation_error_handler(e):
    from app import APP
    APP.logger.warn(e)
    return jsonify(e.messages), 400


def mongo_validation_error_handler(e):
    from app import APP
    APP.logger.warn(e)
    return jsonify(e.args), 400


def error_handler(e):
    from app import APP
    APP.logger.error(e)
    return "Internal error", 500


def not_found(e):
    from app import APP
    APP.logger.info(e)
    return "Not found", 404


exception_handler = {
    MarshmallowValidationError: marshmallow_validation_error_handler,
    MongoValidationError: mongo_validation_error_handler,
    DoesNotExist: not_found,
    Exception: error_handler
}
