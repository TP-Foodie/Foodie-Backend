from models.order import Order
from services.exceptions.order_exceptions import NonExistingOrderException


def list_all():
    return Order.objects


def get_order(order_id):
    return Order.objects.get(id=order_id)


def get_favor_orders():
    return Order.objects.filter(type=Order.FAVOR_TYPE)


def count():
    return Order.objects.count()


def create(order_type, owner, product, number):
    return Order.objects.create(type=order_type, owner=owner, product=product, number=number)


def update(order_id, field, value):
    order = Order.objects.filter(id=order_id).first()

    if not order:
        raise NonExistingOrderException()

    order[field] = value
    order.save()
    return order


def filter_by(params):
    return Order.objects.filter(**params)
