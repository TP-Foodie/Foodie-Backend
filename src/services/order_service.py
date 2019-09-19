from src.models.order import Order
from src.repositories import order_repository


def create(order_type, owner, product):
    order_repository.create(order_type=order_type, owner=owner, product=product, number=order_repository.count() + 1)
