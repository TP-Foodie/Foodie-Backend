from bson.errors import InvalidId
from flask import jsonify, Blueprint
from marshmallow import ValidationError as MarshmallowValidationError
from mongoengine import ValidationError as MongoValidationError
from mongoengine import DoesNotExist

from werkzeug.exceptions import MethodNotAllowed, NotFound

from services.exceptions.order_exceptions import NotEnoughGratitudePointsException
from services.exceptions.unauthorized_user import UnauthorizedUserException
from services.exceptions.invalid_usage_exception import InvalidUsage
from services.exceptions.user_exceptions import NonExistingDeliveryException

from controllers.utils import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, \
    HTTP_405_METHOD_NOT_ALLOWED, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_ERROR

import logger

ERRORS_BLUEPRINT = Blueprint('errors', __name__)


@ERRORS_BLUEPRINT.app_errorhandler(MarshmallowValidationError)
def marshmallow_validation_error_handler(error):
    return jsonify(error.messages), HTTP_400_BAD_REQUEST


@ERRORS_BLUEPRINT.app_errorhandler(MongoValidationError)
def mongo_validation_error_handler(error):
    logger.warn(error)
    return jsonify(error.args), HTTP_400_BAD_REQUEST


@ERRORS_BLUEPRINT.app_errorhandler(Exception)
def error_handler(error):
    logger.error(error)
    return "Internal error", HTTP_500_INTERNAL_ERROR


@ERRORS_BLUEPRINT.app_errorhandler(MethodNotAllowed)
def handle_method_not_allowed(error):
    logger.error(error)
    return "Method not allowed", HTTP_405_METHOD_NOT_ALLOWED


@ERRORS_BLUEPRINT.app_errorhandler(DoesNotExist)
def does_not_exists(error):
    logger.info(error)
    return "Not found", HTTP_404_NOT_FOUND


@ERRORS_BLUEPRINT.app_errorhandler(NotFound)
def not_found(error):
    logger.info(error)
    return "Not found", HTTP_404_NOT_FOUND


@ERRORS_BLUEPRINT.app_errorhandler(InvalidId)
def invalid_id(error):
    logger.info(error)
    return "Invalid id", HTTP_400_BAD_REQUEST


@ERRORS_BLUEPRINT.app_errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    logger.info(error)
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@ERRORS_BLUEPRINT.app_errorhandler(UnauthorizedUserException)
def unauthorized(error):
    logger.info(error)
    return "Unauthorized", HTTP_401_UNAUTHORIZED


@ERRORS_BLUEPRINT.app_errorhandler(NonExistingDeliveryException)
def non_existing_delivery(error):
    logger.info(error)
    return "non existing delivery", HTTP_400_BAD_REQUEST


@ERRORS_BLUEPRINT.app_errorhandler(NotEnoughGratitudePointsException)
def not_enough_gratitude_points_error_handler(error):
    logger.info(error)
    return "Not enough gratitude points", HTTP_400_BAD_REQUEST
