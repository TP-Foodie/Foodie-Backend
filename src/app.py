from flask import Flask, jsonify, request

APP = Flask(__name__)

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