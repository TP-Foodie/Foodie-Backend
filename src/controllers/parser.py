from bson import ObjectId

from src.services.exceptions.product_exceptions import NonExistingPlaceException


def parse_order_request(values):
    if not ObjectId.is_valid(values['product']['place']):
        raise NonExistingPlaceException()

    values.update({'product': {
        'name': values['product']['name'],
        'place': ObjectId(values['product']['place'])
    }})
    return values
