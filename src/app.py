from flask import Flask, json, request, Response

from services.database import DB
from controllers.deliveries_disponibles_controller import deliveries_disponibles_blueprint, COLLECTION_DELIVERIES_DISPONIBLES

APP = Flask(__name__)
APP.register_blueprint(deliveries_disponibles_blueprint, url_prefix='/' + COLLECTION_DELIVERIES_DISPONIBLES)

db = DB.init()
    
if __name__ == '__main__':
    APP.run(host='0.0.0.0', port='5000', debug=True)