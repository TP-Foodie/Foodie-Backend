from flask import Blueprint, jsonify, request, abort

from src.controllers.parser import parse_order_request, parse_take_order_request
from src.controllers.utils import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK
from src.repositories import order_repository
from src.schemas.order import ListOrderSchema, DetailsOrderSchema
from src.services import order_service
from src.services.exceptions.invalid_usage_exception import InvalidUsage
from src.services.exceptions.order_exceptions import NonExistingPlaceException

ORDERS_BLUEPRINT = Blueprint('orders', 'order_controller', url_prefix='/orders')
NO_CONTENT = ''


@ORDERS_BLUEPRINT.route('/', methods=['GET'])
def list_orders():
    data = ListOrderSchema(many=True).dump(order_repository.list_all())
    return jsonify(data)


@ORDERS_BLUEPRINT.route('/', methods=['POST'])
def create_order():
    try:
        order_service.create(*parse_order_request(request.json).values())
    except NonExistingPlaceException:
        raise InvalidUsage("Place does not exists", status_code=HTTP_400_BAD_REQUEST)

    return NO_CONTENT, HTTP_201_CREATED


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
    order_service.take(order_id, parse_take_order_request(request.json))
    return NO_CONTENT, HTTP_200_OK
