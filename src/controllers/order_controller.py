from flask import Blueprint, jsonify, request

from src.repositories import order_repository
from src.schemas.order import ListOrderSchema, DetailsOrderSchema
from src.services import order_service

ORDERS_BLUEPRINT = Blueprint('orders', 'order_controller', url_prefix='/orders')


@ORDERS_BLUEPRINT.route('/', methods=['GET'])
def list_orders():
    data = ListOrderSchema(many=True).dump(order_repository.list_all())
    return jsonify(data)


@ORDERS_BLUEPRINT.route('/', methods=['POST'])
def create_order():
    order_type = request.json.get('order_type')
    owner = request.json.get('owner')
    product = request.json.get('product')
    order_service.create(order_type, owner, product)
    return ''


@ORDERS_BLUEPRINT.route('/<order_id>', methods=['GET'])
def order_details(order_id):
    data = DetailsOrderSchema().dump(order_repository.get_order(order_id))
    return jsonify(data)
