from bson.objectid import ObjectId

from models import Place
from models.order import Product
from services.exceptions.order_exceptions import NonExistingPlaceException


def create(name, place):
    if not ObjectId.is_valid(place) or not Place.objects.filter(id=place):
        raise NonExistingPlaceException()

    return Product.objects.create(name=name, place=place)
