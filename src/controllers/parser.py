from bson import ObjectId


def parse_order_request(values):
    values.update({'product': {
        'name': values['product']['name'],
        'place': ObjectId(values['product']['place'])
    }})
    return values
