from datetime import datetime
from flask import Blueprint, jsonify, request

from controllers.utils import HTTP_200_OK
from logger import log_request_response
from schemas.order import ListOrderSchema
from services import user_service, order_service
from services.auth_service import authenticate

STATISTICS_BLUEPRINT = Blueprint('statistics', __name__)


@STATISTICS_BLUEPRINT.route('/registrations', methods=['GET'])
@log_request_response
@authenticate
def registrations():
    month = int(request.args.get('month', datetime.today().month))
    year = int(request.args.get('year', datetime.today().year))
    return jsonify(user_service.registrations_by_date(month, year)), HTTP_200_OK


@STATISTICS_BLUEPRINT.route('/completed_orders', methods=['GET'])
@log_request_response
@authenticate
def completed_orders():
    return jsonify(order_service.completed_by_date()), HTTP_200_OK


@STATISTICS_BLUEPRINT.route('/cancelled_orders', methods=['GET'])
@log_request_response
@authenticate
def cancelled_orders():
    return jsonify(order_service.cancelled_by_date()), HTTP_200_OK
