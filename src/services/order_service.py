from src.models.order import Order


def create(order_type, owner, product):
    Order.objects.create(type=order_type, owner=owner, product=product, number=1)
