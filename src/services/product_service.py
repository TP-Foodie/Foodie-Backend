from bson.objectid import ObjectId

from models import Place
from models.order import Product
from services.exceptions.order_exceptions import NonExistingPlaceException
from repositories import product_repository


def create(name, place):
    if not ObjectId.is_valid(place) or not Place.objects.filter(id=place):
        raise NonExistingPlaceException()

    return Product.objects.create(name=name, place=place)


def create_product(product_data):
    image = ""
    if product_data.get('image') is not None:
        image = product_data["image"]

    return product_repository.create_product(
        product_data["name"], product_data["description"],
        product_data["price"], product_data["place"], image
    )


def get_products_from_place(id_place):
    return product_repository.get_products_from_place(id_place)
