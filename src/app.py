from flask import Flask, json, request, Response

from database.Database import DB
from models.DeliveryDisponible import DeliveryDisponible

COLLECTION_DELIVERIES_DISPONIBLES = 'deliveries_disponibles'

APP = Flask(__name__)

db = DB.init()

#
#   Endpoint Rest API: Deliveries Disponibles
#
#   POST: agregar delivery como disponible
#   GET: get deliveries disponibles cercanos
#   DELETE: eliminar delivery como disponible
#
@APP.route('/deliveries_disponibles', methods=['GET', 'POST', 'DELETE'])
def deliveries_disponibles():
    if request.method == 'POST':
        # agregar delivery como disponible
        print(request.get_json())
        DB.agregar_documento(COLLECTION_DELIVERIES_DISPONIBLES, request.get_json())
        return myResponse(201, 'Created Succesfully')
    elif request.method == 'GET':
        # get deliveries disponibles cercanos
        query = {'coordinates': {'$within': {'$center': [[0, 0], 5]}}}
        lista_docs = DB.encontrar_lista_documentos(COLLECTION_DELIVERIES_DISPONIBLES, query)
        return myResponse(200, lista_docs)
    elif request.method == 'DELETE':
        # eliminar delivery como disponible
        print(request.get_json())
        DB.eliminar_documento(COLLECTION_DELIVERIES_DISPONIBLES, request.get_json())
        return myResponse(200, 'Deleted Succesfully')


def myResponse(status, body):
    return Response(response=json.dumps({'status': status, 'body': body}), status=status, 
        mimetype='application/json')
    
if __name__ == '__main__':
    APP.run(host='0.0.0.0', port='5000', debug=True)