""" This module handles available deliveries endpoint """

from flask import json, request, Response, Blueprint
from marshmallow import ValidationError

from services.deliveries_disponibles_service import (
    COLLECTION_DELIVERIES_DISPONIBLES, DeliveriesDisponiblesService)
from schemas.delivery_disponible_schema import DeliveryDisponibleSchema
from schemas.query_deliveries_cercanos_schema import QueryDeliveriesCercanosSchema
from schemas.eliminar_delivery_disponible_schema import EliminarDeliveryDisponibleSchema
from my_exceptions.available_deliveries_exceptions import ValidationException

# Flask blueprint
AVAILABLE_DELIVERIES_BLUEPRINT = Blueprint(COLLECTION_DELIVERIES_DISPONIBLES, __name__)

#
#   Endpoints Rest API: Available Deliveries.
#
#   POST: add delivery as available.
#   GET: get nearby available deliveries.
#   DELETE: delete delivery as available
#

@AVAILABLE_DELIVERIES_BLUEPRINT.route(COLLECTION_DELIVERIES_DISPONIBLES, methods=['POST'])
def post():
    """ This methos handle POST in available_deliveries endpoint"""
    # get json data, validates and deserializes it.
    request_data = request.get_json()

    # convert JSON to model object.
    try:
        available_delivery_schema = DeliveryDisponibleSchema()
        available_delivery_data = available_delivery_schema.load(request_data)
    except ValidationError as err:
        raise ValidationException(err.messages)

    # add delivery as available.
    available_deliveries_service = DeliveriesDisponiblesService()
    available_deliveries_service.agregar_delivery_disponible(available_delivery_data)

    return Response(response=json.dumps({'status': 201, 'body': 'Created Succesfully'}), status=201,
                    mimetype='application/json')

@AVAILABLE_DELIVERIES_BLUEPRINT.route(COLLECTION_DELIVERIES_DISPONIBLES, methods=['GET'])
def get():
    """ This methos handle GET in deliveries_disponibles endpoint"""
    # get json data, validates and deserializes it.
    request_data = request.get_json()

    # convert JSON to model object.
    try:
        query_nearby_deliveries_schema = QueryDeliveriesCercanosSchema()
        query_nearby_deliveries_data = query_nearby_deliveries_schema.load(request_data)
    except ValidationError as err:
        raise ValidationException(err.messages)

    # query nearby deliveries.
    available_deliveries_service = DeliveriesDisponiblesService()
    lista_docs = available_deliveries_service.query_deliveries_cercanos(
        query_nearby_deliveries_data)

    return Response(response=json.dumps({'status': 200, 'body': lista_docs}), status=200,
                    mimetype='application/json')

@AVAILABLE_DELIVERIES_BLUEPRINT.route(COLLECTION_DELIVERIES_DISPONIBLES, methods=['DELETE'])
def delete():
    """ This methos handle DELETE in deliveries_disponibles endpoint"""
    # get json data, validates and deserializes it.
    request_data = request.get_json()

    # convert JSON to model object.
    try:
        delete_delivery_as_available_schema = EliminarDeliveryDisponibleSchema()
        delete_delivery_as_available_data = delete_delivery_as_available_schema.load(request_data)
    except ValidationError as err:
        raise ValidationException(err.messages)

    # delete delivery as available.
    available_deliveries_service = DeliveriesDisponiblesService()
    available_deliveries_service.eliminar_delivery_disponible(delete_delivery_as_available_data)

    return Response(response=json.dumps({'status': 200, 'body': 'Deleted Succesfully'}), status=200,
                    mimetype='application/json')
