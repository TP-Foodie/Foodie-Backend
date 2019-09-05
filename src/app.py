from flask import Flask, jsonify, request

from services.DatabaseApi import DatabaseApi
from models.DeliveryDisponible import DeliveryDisponible
from models.Coordinates import Coordinates

APP = Flask(__name__)

db = DatabaseApi('localhost:27017')

#   Endpoint de testing de santiago-alvarezjulia
@APP.route('/test')
def test():
    doc = {'_id': '1', 'name': 'santo'}
    db.agregar_documento('deliveries_disponibles', doc)

    return db.encontrar_documento('deliveries_disponibles', doc)

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
        return db.agregar_documento('deliveries_disponibles', request.json)
    elif request.method == 'GET':
        # get deliveries disponibles cercanos
        query = {'coordinates': {'$within': {'$center': [[0, 0], 5]}}}
        return db.encontrar_lista_documentos('deliveries_disponibles', query)
    elif request.method == 'DELETE':
        # eliminar delivery como disponible
        return {'status': 200, 'body': 'Deleted Succesfully'}
    else:
        # Bad Request
        return {'status': 400, 'body': 'Bad Request'}


if __name__ == '__main__':
    APP.run()