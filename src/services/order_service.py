from src.repositories import order_repository, product_repository


def create(order_type, owner, product):
    created_product = product_repository.get_or_create(*product.values())
    order_repository.create(
        order_type=order_type,
        owner=owner,
        product=created_product.id,
        number=order_repository.count() + 1
    )
