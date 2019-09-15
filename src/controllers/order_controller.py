from flask import Blueprint, jsonify

from src.repositories import order_repository
from src.schemas.order import orders_schema

ORDERS_BLUEPRINT = Blueprint('orders', 'order_controller', url_prefix='/orders')


@ORDERS_BLUEPRINT.route('/', methods=['GET'])
def list_orders():
    data = orders_schema.dump(order_repository.list_all())
    return jsonify(data)
