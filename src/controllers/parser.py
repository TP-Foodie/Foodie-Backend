from bson import ObjectId
from datetime import datetime


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
            },
            'owner': ObjectId(values['user'].id)
        })
    del values['user']
    return values


def parse_take_order_request(values):
    if values.get('delivery'):
        values['delivery'] = ObjectId(values['delivery'])

    return values


def parse_rule_request(values):
    return {
        **values.get('condition', {}),
        **values.get('consequence', {}),
        'name': values.get('name', ''),
    }


def build_quotation_response(price):
    return {'price': price}


def get_month_and_year(request):
    month = int(request.args.get('month', datetime.today().month))
    year = int(request.args.get('year', datetime.today().year))
    return month, year
