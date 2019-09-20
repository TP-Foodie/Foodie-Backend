from bson.objectid import ObjectId

from src.models import Place
from src.services.exceptions.product_exceptions import NonExistingProductException


def create(name, place):
    if not ObjectId.is_valid(place) or not Place.objects.filter(id=place):
        raise NonExistingProductException()
