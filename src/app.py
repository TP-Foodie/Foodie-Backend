from flask import Flask, jsonify, request

from services.DatabaseApi import DatabaseApi
from models.DeliveryDisponible import DeliveryDisponible
from models.Coordinates import Coordinates

APP = Flask(__name__)

@APP.route('/test')
def test():
    
    db = DatabaseApi('localhost:27017')
    #document = DeliveryDisponible('1', 'cacho', 'url_imagen.com', Coordinates(0, 0))

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
        return {'status': 201, 'body': 'Created Succesfully'}
    elif request.method == 'GET':
        # get deliveries disponibles cercanos
        return {'status': 200, 'body': []}
    elif request.method == 'DELETE':
        # eliminar delivery como disponible
        return {'status': 200, 'body': 'Deleted Succesfully'}


if __name__ == '__main__':
    APP.run()