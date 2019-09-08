from flask import Flask, json, request, Response

from repositories.database_api import DB
from deliveries_disponibles.controllers.deliveries_disponibles_controller import deliveries_disponibles_blueprint, COLLECTION_DELIVERIES_DISPONIBLES

# initialize Flask app
APP = Flask(__name__)

# register Flask blueprints
APP.register_blueprint(deliveries_disponibles_blueprint, url_prefix='/' + COLLECTION_DELIVERIES_DISPONIBLES)

# initialize database api
db = DB.init()

if __name__ == "__main__":
    APP.run(host='0.0.0.0', port='5000', debug=True)