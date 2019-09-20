from src.repositories import order_repository


def create(order_type, owner, product):
    created_product = order_repository.get_or_create_product(*product.values())
    order_repository.create(
        order_type=order_type,
        owner=owner,
        product=created_product.id,
        number=order_repository.count() + 1
    )
