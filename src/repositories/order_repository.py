from src.models.order import Order


def list_all():
    return Order.objects


def get_order(order_id):
    return Order.objects.get(id=order_id)
