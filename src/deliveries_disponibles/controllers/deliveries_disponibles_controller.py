from flask import Flask, json, request, Response, Blueprint

from repositories.database_api import DB
from deliveries_disponibles.models.query_deliveries_cercanos import QueryDeliveriesCercanos
from deliveries_disponibles.schemas.delivery_disponible_schema import DeliveryDisponibleSchema
from deliveries_disponibles.schemas.query_deliveries_cercanos_schema import QueryDeliveriesCercanosSchema
from deliveries_disponibles.schemas.borrar_delivery_disponible_schema import BorrarDeliveryDisponibleSchema

# database collection names
COLLECTION_DELIVERIES_DISPONIBLES = 'deliveries_disponibles'

# blueprints Flask
deliveries_disponibles_blueprint = Blueprint(COLLECTION_DELIVERIES_DISPONIBLES, __name__)

# data schemas
delivery_disponible_schema = DeliveryDisponibleSchema()
query_deliveries_cercanos_schema = QueryDeliveriesCercanosSchema()
borrar_delivery_disponible_schema = BorrarDeliveryDisponibleSchema()

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
    delivery_disponible_data = delivery_disponible_schema.load(content)
    
    DB.agregar_documento(COLLECTION_DELIVERIES_DISPONIBLES, delivery_disponible_data)

    return myResponse(201, 'Created Succesfully')

@deliveries_disponibles_blueprint.route('/', methods=['GET'])
def get():
    # get json data, validates and deserializes it
    content = request.get_json()
    query_deliveries_cercanos_data = query_deliveries_cercanos_schema.load(content)

    # create geospatial query
    # TODO: averiguar sobre geospatial indexes (son necesarios?)
    longitude = query_deliveries_cercanos_data['coordinates'][0]
    latitude = query_deliveries_cercanos_data['coordinates'][1]
    radius = query_deliveries_cercanos_data['radius']
    query = {'coordinates': {'$geoWithin': {'$center': [[longitude, latitude], radius]}}}

    # run the geospatial query
    lista_docs = DB.encontrar_lista_documentos(COLLECTION_DELIVERIES_DISPONIBLES, query)

    return myResponse(200, lista_docs)

@deliveries_disponibles_blueprint.route('/', methods=['DELETE'])
def delete():
    # get json data, validates and deserializes it
    content = request.get_json()
    borrar_delivery_disponible_data = borrar_delivery_disponible_schema.load(content)

    # elimino el delivery disponible de la database
    DB.eliminar_documento(COLLECTION_DELIVERIES_DISPONIBLES, borrar_delivery_disponible_data)

    return myResponse(200, 'Deleted Succesfully')

def myResponse(status, body):
    return Response(response=json.dumps({'status': status, 'body': body}), status=status, 
        mimetype='application/json')