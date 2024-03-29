""" This module handles available deliveries endpoint """

from flask import request, jsonify, Blueprint

from controllers.parser import parse_available_deliveries_request
from logger import log_request_response
from schemas.user import DeliveryProfile
from schemas.query_nearby_deliveries_schema import QueryNearbyDeliveriesSchema
from services import delivery_service

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
    deliveries = delivery_service.query_nearby_deliveries(
        query_nearby_deliveries_data)

    return jsonify({'body': DeliveryProfile().dump(deliveries, many=True)}), 200
