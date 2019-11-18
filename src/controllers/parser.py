from bson import ObjectId


def parse_available_deliveries_request(values):
    radius = values["radius"]
    latitude = values["latitude"]
    longitude = values["longitude"]
    coordinates = [latitude, longitude]
    return {'radius': radius, 'coordinates': coordinates}


def parse_order_request(values):
    values.update(
        {
            'product': {
                'name': values['product']['name'],
                'place': ObjectId(values['product']['place']),
                'description': values['product']['description'],
                'price': values['product']['price'],
                'image': values['product']['image']
            },
            'owner': ObjectId(values['user'].id)
        })
    del values['user']
    return values


def parse_take_order_request(values):
    if values.get('delivery', None) is None:
        delivery = None
    else:
        delivery = ObjectId(values['delivery'])

    values.update({
        'status': values['status'],
        'delivery': delivery,
        'id_chat': values.get('id_chat', None),
        'payment_method': values.get('payment_method', None)
    })
    return values


def parse_rule_request(values):
    return {
        **values.get('condition', {}),
        **values.get('consequence', {}),
        'name': values.get('name', ''),
    }
