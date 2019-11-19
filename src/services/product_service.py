from bson.objectid import ObjectId

from models.place import Place
from models.order import Product
from services.exceptions.order_exceptions import NonExistingPlaceException
from repositories import product_repository


def create(name, place):
    if not ObjectId.is_valid(place) or not Place.objects.filter(id=place):
        raise NonExistingPlaceException()

    return Product.objects.create(name=name, place=place)


def get_products_from_place(id_place):
    return product_repository.get_products_from_place(id_place)
