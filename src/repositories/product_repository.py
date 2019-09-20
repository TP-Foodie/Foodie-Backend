from src.models.order import Product


def get_or_create(name, place):
    product = Product.objects.filter(name=name, place=place).first()
    return product if product else Product.objects.create(name=name, place=place)


def count():
    return Product.objects.count()
