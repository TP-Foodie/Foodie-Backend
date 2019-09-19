from src.models.order import Order


def list_all():
    return Order.objects


def get_order(order_id):
    return Order.objects.get(id=order_id)


def count():
    return Order.objects.count()


def create(order_type, owner, product, number):
    return Order.objects.create(type=order_type, owner=owner, product=product, number=number)
