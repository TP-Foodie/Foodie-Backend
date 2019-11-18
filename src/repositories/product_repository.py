from models.product import Product
from services import product_service


def get_or_create(name, place):
    product = Product.objects.filter(name=name, place=place).first()
    return product if product else product_service.create(name=name, place=place)


def count():
    return Product.objects.count()


def create_product(name, description, price, place, image):
    return Product.objects.create(
        name=name, description=description, price=price, place=place, image=image
    )


def get_products_from_place(id_place):
    return Product.objects(place__id=id_place)
