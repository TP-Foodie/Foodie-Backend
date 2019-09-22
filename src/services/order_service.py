from src.models.order import Order
from src.repositories import order_repository, product_repository


def create(order_type, owner, product):
    created_product = product_repository.get_or_create(*product.values())
    order_repository.create(
        order_type=order_type,
        owner=owner,
        product=created_product.id,
        number=order_repository.count() + 1
    )


def take(order_id, new_data):
    order_repository.update(order_id, 'status', new_data.get('status', Order.WAITING_STATUS))
