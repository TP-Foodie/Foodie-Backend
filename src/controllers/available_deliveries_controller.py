""" This module handles available deliveries endpoint """

from flask import request, jsonify, Blueprint

from services import available_deliveries_service
from schemas.available_delivery_schema import AvailableDeliverySchema
from schemas.query_nearby_deliveries_schema import QueryNearbyDeliveriesSchema
from schemas.delete_available_delivery_schema import DeleteAvailableDeliverySchema

# Flask blueprint
AVAILABLE_DELIVERIES_ROUTE = 'available_deliveries'
AVAILABLE_DELIVERIES_BLUEPRINT = Blueprint(AVAILABLE_DELIVERIES_ROUTE, __name__)

#
#   Endpoints Rest API: Available Deliveries.
#
#   POST: add delivery as available.
#   GET: get nearby available deliveries.
#   DELETE: delete delivery as available
#


@AVAILABLE_DELIVERIES_BLUEPRINT.route(AVAILABLE_DELIVERIES_ROUTE, methods=['POST'])
def post():
    """ This methos handle POST in available_deliveries endpoint"""
    # get json data, validates and deserializes it.
    request_data = request.get_json()

    # convert JSON to dict.
    available_delivery_schema = AvailableDeliverySchema()
    available_delivery = available_delivery_schema.load(request_data)

    # add delivery as available.
    available_deliveries_service.add_available_delivery(available_delivery)

    return jsonify({'body': 'Created Succesfully'}), 201


@AVAILABLE_DELIVERIES_BLUEPRINT.route(AVAILABLE_DELIVERIES_ROUTE, methods=['GET'])
def get():
    """ This methos handle GET in deliveries_disponibles endpoint"""
    # get json data, validates and deserializes it.
    request_data = request.get_json()

    # convert JSON to dict.
    query_nearby_deliveries_schema = QueryNearbyDeliveriesSchema()
    query_nearby_deliveries_data = query_nearby_deliveries_schema.load(request_data)

    # query nearby deliveries.
    lista_docs = available_deliveries_service.query_nearby_deliveries(
        query_nearby_deliveries_data)

    return jsonify({'body': lista_docs}), 200


@AVAILABLE_DELIVERIES_BLUEPRINT.route(AVAILABLE_DELIVERIES_ROUTE, methods=['DELETE'])
def delete():
    """ This methos handle DELETE in deliveries_disponibles endpoint"""
    # get json data, validates and deserializes it.
    request_data = request.get_json()

    # convert JSON to dict.
    delete_delivery_as_available_schema = DeleteAvailableDeliverySchema()
    delete_delivery_as_available_data = delete_delivery_as_available_schema.load(request_data)

    # delete delivery as available.
    available_deliveries_service.delete_available_delivery(delete_delivery_as_available_data)

    return jsonify({'body': 'Deleted Succesfully'}), 200
