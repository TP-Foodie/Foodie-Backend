from models.product import Product
from models.place import Place


def count():
    return Product.objects.count()


def get_products_from_place(id_place):
    places = Place.objects(id=id_place)
    return Product.objects(place__in=places)
