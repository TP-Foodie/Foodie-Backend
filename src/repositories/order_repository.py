from src.models.order import Order, Product


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


def get_or_create_product(name, place):
    product = Product.objects.filter(name=name, place=place).first()
    return product if product else Product.objects.create(name=name, place=place)


def products_count():
    return Product.objects.count()
