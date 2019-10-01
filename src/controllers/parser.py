from bson import ObjectId


def parse_order_request(values):
    values.update({'product': {
        'name': values['product']['name'],
        'place': ObjectId(values['product']['place'])
    }})
    return values


def parse_take_order_request(values):
    values.update({
        'status': values['status'],
        'delivery': ObjectId(values['delivery'])
    })
    return values


def parse_rule_request(values):
    return {
        **values['condition'],
        **values['consequence'],
        'name': values['name'],
    }
