from flask import Blueprint, jsonify, request

from controllers.parser import parse_order_request, parse_take_order_request
from controllers.utils import HTTP_201_CREATED, \
    HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_404_NOT_FOUND
from logger import log_request_response
from repositories import order_repository
from schemas.order import ListOrderSchema, DetailsOrderSchema
from services import order_service
from services.exceptions.invalid_usage_exception import InvalidUsage
from services.exceptions.user_exceptions import NonExistingDeliveryException
from services.exceptions.order_exceptions import NonExistingPlaceException, \
    NonExistingOrderException
from services.auth_service import authenticate
from services.rule_service import RuleService

ORDERS_BLUEPRINT = Blueprint('orders', 'order_controller')


rule_service = RuleService()  # pylint: disable=invalid-name


@ORDERS_BLUEPRINT.route('/', methods=['GET'])
@log_request_response
@authenticate
def list_orders():
    data = ListOrderSchema(many=True).dump(order_repository.list_all())
    return jsonify(data)


@ORDERS_BLUEPRINT.route('/', methods=['POST'])
@log_request_response
@authenticate
def create_order(user):
    try:
        parsed_data = parse_order_request({**request.json, 'user': user})
        order = order_service.create(**parsed_data)
        data = DetailsOrderSchema().dump(order)
    except NonExistingPlaceException:
        raise InvalidUsage("Place does not exists", status_code=HTTP_400_BAD_REQUEST)

    return jsonify(data), HTTP_201_CREATED


@ORDERS_BLUEPRINT.route('/<order_id>', methods=['GET'])
@log_request_response
@authenticate
def order_details(order_id):
    data = DetailsOrderSchema().dump(order_repository.get_order(order_id))
    return jsonify(data)


@ORDERS_BLUEPRINT.route('/<order_id>/quotation', methods=['GET'])
@authenticate
def order_quotation(order_id):
    return jsonify(rule_service.quote_price(order_id))


@ORDERS_BLUEPRINT.route('/favors', methods=['GET'])
@log_request_response
@authenticate
def list_favor_orders():
    data = ListOrderSchema(many=True).dump(order_repository.get_favor_orders())
    return jsonify(data)


@ORDERS_BLUEPRINT.route('/placed', methods=['GET'])
@log_request_response
@authenticate
def list_placed_orders(user):
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    data = ListOrderSchema(many=True).dump(order_service.placed_by(user.id, start_date, end_date))
    return jsonify(data)


@ORDERS_BLUEPRINT.route('/<order_id>', methods=['PATCH'])
@log_request_response
@authenticate
def update_order(order_id):
    try:
        order = order_service.take(order_id, parse_take_order_request(request.json))
        data = DetailsOrderSchema().dump(order)
    except NonExistingDeliveryException:
        raise InvalidUsage('Delivery does not exists', status_code=HTTP_400_BAD_REQUEST)
    except NonExistingOrderException:
        raise InvalidUsage('Order does not exists', status_code=HTTP_404_NOT_FOUND)

    return jsonify(data), HTTP_200_OK
