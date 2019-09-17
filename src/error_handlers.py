from flask import jsonify, Blueprint
from marshmallow import ValidationError as MarshmallowValidationError
from mongoengine import ValidationError as MongoValidationError
from mongoengine import DoesNotExist

import logger

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
