from flask import jsonify
from marshmallow import ValidationError as MarshmallowValidationError
from mongoengine import ValidationError as MongoValidationError
from mongoengine import DoesNotExist

import logger


def marshmallow_validation_error_handler(error):
    return jsonify(error.messages), 400


def mongo_validation_error_handler(error):
    logger.warn(error)
    return jsonify(error.args), 400


def error_handler(error):
    logger.error(error)
    return "Internal error", 500


def not_found(error):
    logger.info(error)
    return "Not found", 404


EXCEPTION_HANDLER = {
    MarshmallowValidationError: marshmallow_validation_error_handler,
    MongoValidationError: mongo_validation_error_handler,
    DoesNotExist: not_found,
    Exception: error_handler
}
