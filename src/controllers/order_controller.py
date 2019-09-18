from flask import Blueprint, jsonify

from src.repositories import order_repository
from src.schemas.order import ListOrderSchema, DetailsOrderSchema

ORDERS_BLUEPRINT = Blueprint('orders', 'order_controller', url_prefix='/orders')


@ORDERS_BLUEPRINT.route('/', methods=['GET'])
def list_orders():
    data = ListOrderSchema(many=True).dump(order_repository.list_all())
    return jsonify(data)


@ORDERS_BLUEPRINT.route('/<order_id>', methods=['GET'])
def order_details(order_id):
    data = DetailsOrderSchema().dump(order_repository.get_order(order_id))
    return jsonify(data)
