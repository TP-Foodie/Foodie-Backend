""" This module handles deliveries disponibles endpoint """

from flask import json, request, Response, Blueprint
from marshmallow import ValidationError

from services.deliveries_disponibles_service import (
    COLLECTION_DELIVERIES_DISPONIBLES, DeliveriesDisponiblesService)
from schemas.delivery_disponible_schema import DeliveryDisponibleSchema
from schemas.query_deliveries_cercanos_schema import QueryDeliveriesCercanosSchema
from schemas.eliminar_delivery_disponible_schema import EliminarDeliveryDisponibleSchema
from my_exceptions.deliveries_disponibles_exceptions import ValidationException

# blueprints Flask
DELIVERIES_DISPONIBLES_BLUEPRINT = Blueprint(COLLECTION_DELIVERIES_DISPONIBLES, __name__)

#
#   Endpoints Rest API: Deliveries Disponibles
#
#   POST: agregar delivery como disponible
#   GET: get deliveries disponibles cercanos
#   DELETE: eliminar delivery como disponible
#
@DELIVERIES_DISPONIBLES_BLUEPRINT.route(COLLECTION_DELIVERIES_DISPONIBLES, methods=['POST'])
def post():
    """ This methos handle POST in deliveries_disponibles endpoint"""
    # get json data, validates and deserializes it
    content = request.get_json()

    # convert JSON to model object
    try:
        delivery_disponible_schema = DeliveryDisponibleSchema()
        delivery_disponible_data = delivery_disponible_schema.load(content)
    except ValidationError as err:
        raise ValidationException(err.messages)

    # agregar delivery disponible
    deliveries_disponibles_service = DeliveriesDisponiblesService()
    deliveries_disponibles_service.agregar_delivery_disponible(delivery_disponible_data)

    return Response(response=json.dumps({'status': 201, 'body': 'Created Succesfully'}), status=201,
                    mimetype='application/json')

@DELIVERIES_DISPONIBLES_BLUEPRINT.route(COLLECTION_DELIVERIES_DISPONIBLES, methods=['GET'])
def get():
    """ This methos handle GET in deliveries_disponibles endpoint"""
    # get json data, validates and deserializes it
    content = request.get_json()

    # convert JSON to model object
    try:
        query_deliveries_cercanos_schema = QueryDeliveriesCercanosSchema()
        query_deliveries_cercanos_data = query_deliveries_cercanos_schema.load(content)
    except ValidationError as err:
        raise ValidationException(err.messages)

    # query de deliveries cercanos
    deliveries_disponibles_service = DeliveriesDisponiblesService()
    lista_docs = deliveries_disponibles_service.query_deliveries_cercanos(
        query_deliveries_cercanos_data)

    return Response(response=json.dumps({'status': 200, 'body': lista_docs}), status=200,
                    mimetype='application/json')

@DELIVERIES_DISPONIBLES_BLUEPRINT.route(COLLECTION_DELIVERIES_DISPONIBLES, methods=['DELETE'])
def delete():
    """ This methos handle DELETE in deliveries_disponibles endpoint"""
    # get json data, validates and deserializes it
    content = request.get_json()

    # convert JSON to model object
    try:
        eliminar_delivery_disponible_schema = EliminarDeliveryDisponibleSchema()
        eliminar_delivery_disponible_data = eliminar_delivery_disponible_schema.load(content)
    except ValidationError as err:
        raise ValidationException(err.messages)

    # elimino el delivery disponible
    deliveries_disponibles_service = DeliveriesDisponiblesService()
    deliveries_disponibles_service.eliminar_delivery_disponible(eliminar_delivery_disponible_data)

    return Response(response=json.dumps({'status': 200, 'body': 'Deleted Succesfully'}), status=200,
                    mimetype='application/json')
