from flask import Flask, json, request, Response, Blueprint
from marshmallow import ValidationError

from deliveries_disponibles.services.deliveries_disponibles_service import COLLECTION_DELIVERIES_DISPONIBLES, DeliveriesDisponiblesService
from deliveries_disponibles.models.query_deliveries_cercanos import QueryDeliveriesCercanos
from deliveries_disponibles.schemas.delivery_disponible_schema import DeliveryDisponibleSchema
from deliveries_disponibles.schemas.query_deliveries_cercanos_schema import QueryDeliveriesCercanosSchema
from deliveries_disponibles.schemas.borrar_delivery_disponible_schema import BorrarDeliveryDisponibleSchema
from deliveries_disponibles.exceptions import ValidationException

# blueprints Flask
deliveries_disponibles_blueprint = Blueprint(COLLECTION_DELIVERIES_DISPONIBLES, __name__)

# data schemas
delivery_disponible_schema = DeliveryDisponibleSchema()
query_deliveries_cercanos_schema = QueryDeliveriesCercanosSchema()
borrar_delivery_disponible_schema = BorrarDeliveryDisponibleSchema()

# services
deliveries_disponibles_service = DeliveriesDisponiblesService()

#
#   Endpoints Rest API: Deliveries Disponibles
#
#   POST: agregar delivery como disponible
#   GET: get deliveries disponibles cercanos
#   DELETE: eliminar delivery como disponible
#
@deliveries_disponibles_blueprint.route('/', methods=['POST'])
def post():
    # get json data, validates and deserializes it
    content = request.get_json()
    
    try:
        delivery_disponible_data = delivery_disponible_schema.load(content)
    except ValidationError as err:
        raise ValidationException(err.messages)

    # agregar delivery disponible
    deliveries_disponibles_service.agregar_delivery_disponible(delivery_disponible_data)

    return myResponse(201, 'Created Succesfully')

@deliveries_disponibles_blueprint.route('/', methods=['GET'])
def get():
    # get json data, validates and deserializes it
    content = request.get_json()

    try:
        query_deliveries_cercanos_data = query_deliveries_cercanos_schema.load(content)
    except ValidationError as err:
        raise ValidationException(err.messages)

    # query de deliveries cercanos
    lista_docs = deliveries_disponibles_service.query_deliveries_cercanos(query_deliveries_cercanos_data)

    return myResponse(200, lista_docs)

@deliveries_disponibles_blueprint.route('/', methods=['DELETE'])
def delete():
    # get json data, validates and deserializes it
    content = request.get_json()
    
    try:
        borrar_delivery_disponible_data = borrar_delivery_disponible_schema.load(content)
    except ValidationError as err:
        raise ValidationException(err.messages)
    
    # elimino el delivery disponible
    deliveries_disponibles_service.borrar_delivery_disponible(borrar_delivery_disponible_data)

    return myResponse(200, 'Deleted Succesfully')

def myResponse(status, body):
    return Response(response=json.dumps({'status': status, 'body': body}), status=status, 
        mimetype='application/json')