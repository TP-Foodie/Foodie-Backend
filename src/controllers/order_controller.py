from flask import Blueprint

ORDERS_BLUEPRINT = Blueprint('orders', __name__, url_prefix='/orders')


@ORDERS_BLUEPRINT.route('/', methods=['GET'])
def list_orders():
    return ''
