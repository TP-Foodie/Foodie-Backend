from src.models.order import Order, Product


def list_all():
    return Order.objects


def get_order(order_id):
    return Order.objects.get(id=order_id)


def count():
    return Order.objects.count()


def create(order_type, owner, product, number):
    return Order.objects.create(type=order_type, owner=owner, product=product, number=number)


def get_or_create_product(name, place):
    return Product.objects(name=name, place=place).modify(upsert=True, new=True, set__name=name, set__place=place)


def products_count():
    return Product.objects.count()
