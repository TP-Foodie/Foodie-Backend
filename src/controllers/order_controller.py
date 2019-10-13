from flask import Blueprint, jsonify, request

from controllers.parser import parse_order_request, parse_take_order_request
from controllers.utils import HTTP_201_CREATED, \
    HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_404_NOT_FOUND
from repositories import order_repository
from schemas.order import ListOrderSchema, DetailsOrderSchema
from services import order_service
from services.exceptions.invalid_usage_exception import InvalidUsage
from services.exceptions.user_exceptions import NonExistingDeliveryException
from services.exceptions.order_exceptions import NonExistingPlaceException, \
    NonExistingOrderException
from services.auth_service import authenticate

ORDERS_BLUEPRINT = Blueprint('orders', 'order_controller')


@ORDERS_BLUEPRINT.route('/', methods=['GET'])
@authenticate
def list_orders():
    data = ListOrderSchema(many=True).dump(order_repository.list_all())
    return jsonify(data)


@ORDERS_BLUEPRINT.route('/', methods=['POST'])
def create_order():
    try:
        order = order_service.create(*parse_order_request(request.json).values())
        data = DetailsOrderSchema().dump(order)
    except NonExistingPlaceException:
        raise InvalidUsage("Place does not exists", status_code=HTTP_400_BAD_REQUEST)

    return jsonify(data), HTTP_201_CREATED


@ORDERS_BLUEPRINT.route('/<order_id>', methods=['GET'])
def order_details(order_id):
    data = DetailsOrderSchema().dump(order_repository.get_order(order_id))
    return jsonify(data)


@ORDERS_BLUEPRINT.route('/favors', methods=['GET'])
def list_favor_orders():
    data = ListOrderSchema(many=True).dump(order_repository.get_favor_orders())
    return jsonify(data)


@ORDERS_BLUEPRINT.route('/<order_id>', methods=['PATCH'])
def update_order(order_id):
    try:
        order = order_service.take(order_id, parse_take_order_request(request.json))
        data = DetailsOrderSchema().dump(order)
    except NonExistingDeliveryException:
        raise InvalidUsage('Delivery does not exists', status_code=HTTP_400_BAD_REQUEST)
    except NonExistingOrderException:
        raise InvalidUsage('Order does not exists', status_code=HTTP_404_NOT_FOUND)

    return jsonify(data), HTTP_200_OK
