from bson.errors import InvalidId
from flask import jsonify, Blueprint
from marshmallow import ValidationError as MarshmallowValidationError
from mongoengine import ValidationError as MongoValidationError
from mongoengine import DoesNotExist

import logger

from src.services.exceptions.invalid_usage_exception import InvalidUsage

ERRORS_BLUEPRINT = Blueprint('errors', __name__)


@ERRORS_BLUEPRINT.app_errorhandler(MarshmallowValidationError)
def marshmallow_validation_error_handler(error):
    return jsonify(error.messages), 400


@ERRORS_BLUEPRINT.app_errorhandler(MongoValidationError)
def mongo_validation_error_handler(error):
    logger.warn(error)
    return jsonify(error.args), 400


@ERRORS_BLUEPRINT.app_errorhandler(Exception)
def error_handler(error):
    logger.error(error)
    return "Internal error", 500


@ERRORS_BLUEPRINT.app_errorhandler(DoesNotExist)
def not_found(error):
    logger.info(error)
    return "Not found", 404


@ERRORS_BLUEPRINT.app_errorhandler(InvalidId)
def invalid_id(error):
    logger.info(error)
    return "Invalid id", 400


@ERRORS_BLUEPRINT.app_errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    logger.info(error)
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
