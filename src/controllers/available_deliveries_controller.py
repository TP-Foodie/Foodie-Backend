""" This module handles available deliveries endpoint """

from flask import request, jsonify, Blueprint

from controllers.parser import parse_available_deliveries_request
from logger import log_request_response
from services import available_deliveries_service
from schemas.user import UserProfile
from schemas.query_nearby_deliveries_schema import QueryNearbyDeliveriesSchema

# Flask blueprint
AVAILABLE_DELIVERIES_ROUTE = 'available_deliveries'
AVAILABLE_DELIVERIES_BLUEPRINT = Blueprint(AVAILABLE_DELIVERIES_ROUTE, __name__)

#
#   Endpoints Rest API: Available Deliveries.
#
#   GET: get nearby available deliveries.
#


@AVAILABLE_DELIVERIES_BLUEPRINT.route(AVAILABLE_DELIVERIES_ROUTE, methods=['GET'])
@log_request_response
def get():
    """ This methos handle GET in deliveries_disponibles endpoint"""
    # get json data, validates and deserializes it.
    request_data = parse_available_deliveries_request(request.args)

    # convert JSON to dict.
    query_nearby_deliveries_schema = QueryNearbyDeliveriesSchema()
    query_nearby_deliveries_data = query_nearby_deliveries_schema.load(request_data)

    # query nearby deliveries.
    deliveries = available_deliveries_service.query_nearby_deliveries(
        query_nearby_deliveries_data)

    schema = UserProfile()

    deliveries = [schema.dump(user) for user in deliveries]

    return jsonify({'body': deliveries}), 200
