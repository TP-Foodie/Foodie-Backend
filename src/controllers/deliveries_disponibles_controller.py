from flask import Flask, json, request, Response, Blueprint

from services.database import DB

COLLECTION_DELIVERIES_DISPONIBLES = 'deliveries_disponibles'

deliveries_disponibles_blueprint = Blueprint(COLLECTION_DELIVERIES_DISPONIBLES, __name__)

#
#   Endpoint Rest API: Deliveries Disponibles
#
#   POST: agregar delivery como disponible
#   GET: get deliveries disponibles cercanos
#   DELETE: eliminar delivery como disponible
#
@deliveries_disponibles_blueprint.route('/', methods=['POST'])
def post():
    # agregar delivery como disponible
    print(request.get_json())
    DB.agregar_documento(COLLECTION_DELIVERIES_DISPONIBLES, request.get_json())
    return myResponse(201, 'Created Succesfully')

@deliveries_disponibles_blueprint.route('/', methods=['GET'])
def get():
    # get deliveries disponibles cercanos
    query = {'coordinates': {'$within': {'$center': [[0, 0], 5]}}}
    lista_docs = DB.encontrar_lista_documentos(COLLECTION_DELIVERIES_DISPONIBLES, query)
    return myResponse(200, lista_docs)

@deliveries_disponibles_blueprint.route('/', methods=['DELETE'])
def delete():
    # eliminar delivery como disponible
    print(request.get_json())
    DB.eliminar_documento(COLLECTION_DELIVERIES_DISPONIBLES, request.get_json())
    return myResponse(200, 'Deleted Succesfully')

def myResponse(status, body):
    return Response(response=json.dumps({'status': status, 'body': body}), status=status, 
        mimetype='application/json')