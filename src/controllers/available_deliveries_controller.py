""" This module handles available deliveries endpoint """

from flask import json, request, Response, Blueprint
from marshmallow import ValidationError

from services.available_deliveries_service import (
    AVAILABLE_DELIVERIES_COLLECTION, AvailableDeliveriesService)
from schemas.available_delivery_schema import AvailableDeliverySchema
from schemas.query_nearby_deliveries_schema import QueryNearbyDeliveriesSchema
from schemas.delete_available_delivery_schema import DeleteAvailableDeliverySchema
from my_exceptions.available_deliveries_exceptions import ValidationException

# Flask blueprint
AVAILABLE_DELIVERIES_BLUEPRINT = Blueprint(AVAILABLE_DELIVERIES_COLLECTION, __name__)

#
#   Endpoints Rest API: Available Deliveries.
#
#   POST: add delivery as available.
#   GET: get nearby available deliveries.
#   DELETE: delete delivery as available
#

@AVAILABLE_DELIVERIES_BLUEPRINT.route(AVAILABLE_DELIVERIES_COLLECTION, methods=['POST'])
def post():
    """ This methos handle POST in available_deliveries endpoint"""
    # get json data, validates and deserializes it.
    request_data = request.get_json()

    # convert JSON to model object.
    try:
        available_delivery_schema = AvailableDeliverySchema()
        available_delivery_data = available_delivery_schema.load(request_data)
    except ValidationError as err:
        raise ValidationException(err.messages)

    # add delivery as available.
    available_deliveries_service = AvailableDeliveriesService()
    available_deliveries_service.add_available_delivery(available_delivery_data)

    return Response(response=json.dumps({'status': 201, 'body': 'Created Succesfully'}), status=201,
                    mimetype='application/json')

@AVAILABLE_DELIVERIES_BLUEPRINT.route(AVAILABLE_DELIVERIES_COLLECTION, methods=['GET'])
def get():
    """ This methos handle GET in deliveries_disponibles endpoint"""
    # get json data, validates and deserializes it.
    request_data = request.get_json()

    # convert JSON to model object.
    try:
        query_nearby_deliveries_schema = QueryNearbyDeliveriesSchema()
        query_nearby_deliveries_data = query_nearby_deliveries_schema.load(request_data)
    except ValidationError as err:
        raise ValidationException(err.messages)

    # query nearby deliveries.
    available_deliveries_service = AvailableDeliveriesService()
    lista_docs = available_deliveries_service.query_nearby_deliveries(
        query_nearby_deliveries_data)

    return Response(response=json.dumps({'status': 200, 'body': lista_docs}), status=200,
                    mimetype='application/json')

@AVAILABLE_DELIVERIES_BLUEPRINT.route(AVAILABLE_DELIVERIES_COLLECTION, methods=['DELETE'])
def delete():
    """ This methos handle DELETE in deliveries_disponibles endpoint"""
    # get json data, validates and deserializes it.
    request_data = request.get_json()

    # convert JSON to model object.
    try:
        delete_delivery_as_available_schema = DeleteAvailableDeliverySchema()
        delete_delivery_as_available_data = delete_delivery_as_available_schema.load(request_data)
    except ValidationError as err:
        raise ValidationException(err.messages)

    # delete delivery as available.
    available_deliveries_service = AvailableDeliveriesService()
    available_deliveries_service.delete_available_delivery(delete_delivery_as_available_data)

    return Response(response=json.dumps({'status': 200, 'body': 'Deleted Succesfully'}), status=200,
                    mimetype='application/json')
