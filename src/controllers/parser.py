from bson import ObjectId


def parse_available_deliveries_request(values):
    radius = values["radius"]
    latitude = values["latitude"]
    longitude = values["longitude"]
    coordinates = [latitude, longitude]
    return {'radius': radius, 'coordinates': coordinates}


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
