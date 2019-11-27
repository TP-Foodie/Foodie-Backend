from flask import Blueprint, jsonify, request

from controllers.parser import get_month_and_year
from controllers.utils import HTTP_200_OK
from logger import log_request_response
from services import user_service, order_service
from services.auth_service import authenticate

STATISTICS_BLUEPRINT = Blueprint('statistics', __name__)


@STATISTICS_BLUEPRINT.route('/registrations', methods=['GET'])
@log_request_response
@authenticate
def registrations():
    month, year = get_month_and_year(request)
    return jsonify(user_service.registrations_by_date(month, year)), HTTP_200_OK


@STATISTICS_BLUEPRINT.route('/completed_orders', methods=['GET'])
@log_request_response
@authenticate
def completed_orders():
    month, year = get_month_and_year(request)
    return jsonify(order_service.completed_by_date(month, year)), HTTP_200_OK


@STATISTICS_BLUEPRINT.route('/cancelled_orders', methods=['GET'])
@log_request_response
@authenticate
def cancelled_orders():
    return jsonify(order_service.cancelled_by_date()), HTTP_200_OK
