from models.product import Product
from models.place import Place
from services import product_service


def get_or_create(name, place):
    product = Product.objects.filter(name=name, place=place).first()
    return product if product else product_service.create(name=name, place=place)


def count():
    return Product.objects.count()


def get_products_from_place(id_place):
    places = Place.objects(id=id_place)
    return Product.objects(place__in=places)
