from bson.objectid import ObjectId

from src.models import Place
from src.models.order import Product
from src.services.exceptions.product_exceptions import NonExistingPlaceException


def create(name, place):
    if not ObjectId.is_valid(place) or not Place.objects.filter(id=place):
        raise NonExistingPlaceException()

    return Product.objects.create(name=name, place=place)
