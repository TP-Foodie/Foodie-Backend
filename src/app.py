from flask import Flask, jsonify, request, Response

from services.DatabaseApi import DatabaseApi
from models.DeliveryDisponible import DeliveryDisponible

COLLECTION_DELIVERIES_DISPONIBLES = 'deliveries_disponibles'

APP = Flask(__name__)

db = DatabaseApi('localhost:27017')

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
        db.agregar_documento(COLLECTION_DELIVERIES_DISPONIBLES, request.get_json())
        return {'status': '201', 'body': 'Created Succesfully'}
    elif request.method == 'GET':
        # get deliveries disponibles cercanos
        query = {'coordinates': {'$within': {'$center': [[0, 0], 5]}}}
        lista_docs = db.encontrar_lista_documentos(COLLECTION_DELIVERIES_DISPONIBLES, query)
        return {'status': 200, 'body': lista_docs}
    elif request.method == 'DELETE':
        # eliminar delivery como disponible
        db.eliminar_documento(COLLECTION_DELIVERIES_DISPONIBLES, request.get_json())
        return {'status': 200, 'body': 'Deleted Succesfully'}
    else:
        # Bad Request
        return {'status': 400, 'body': 'Bad Request'}


if __name__ == '__main__':
    APP.run()