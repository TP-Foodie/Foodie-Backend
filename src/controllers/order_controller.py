from flask import Blueprint, jsonify, request

from src.controllers.utils import HTTP_201_CREATED
from src.repositories import order_repository
from src.schemas.order import ListOrderSchema, DetailsOrderSchema
from src.services import order_service

ORDERS_BLUEPRINT = Blueprint('orders', 'order_controller', url_prefix='/orders')
NO_CONTENT = ''

@ORDERS_BLUEPRINT.route('/', methods=['GET'])
def list_orders():
    data = ListOrderSchema(many=True).dump(order_repository.list_all())
    return jsonify(data)


@ORDERS_BLUEPRINT.route('/', methods=['POST'])
def create_order():
    order_service.create(*request.json.values())
    return NO_CONTENT, HTTP_201_CREATED


@ORDERS_BLUEPRINT.route('/<order_id>', methods=['GET'])
def order_details(order_id):
    data = DetailsOrderSchema().dump(order_repository.get_order(order_id))
    return jsonify(data)
