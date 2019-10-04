from models.order import Product
from services import product_service


def get_or_create(name, place):
    product = Product.objects.filter(name=name, place=place).first()
    return product if product else product_service.create(name=name, place=place)


def count():
    return Product.objects.count()
