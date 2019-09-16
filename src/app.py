"""This module initiates Flask APP."""

import os
from flask import Flask
from encoders import CustomJSONEncoder
from flask_cors import CORS
from controllers.places_controller import PLACES_BLUEPRINT
from controllers.users_controller import USERS_BLUEPRINT

from repositories.database_api import DB
from controllers.available_deliveries_controller import AVAILABLE_DELIVERIES_BLUEPRINT
from exceptions_handlers.available_deliveries_exceptions_handler import (
    AVAILABLE_DELIVERIES_EXCEPTIONS_HANDLER)

# initialize Flask app
APP = Flask(__name__)
CORS(APP)

# set default api VERSION to v1
VERSION = os.environ.get('API_VERSION', 'v1')
PREFIX = f"/api/{VERSION}"

# register Flask blueprints
APP.register_blueprint(AVAILABLE_DELIVERIES_BLUEPRINT, url_prefix=f'{PREFIX}/')
APP.register_blueprint(AVAILABLE_DELIVERIES_EXCEPTIONS_HANDLER)
APP.register_blueprint(PLACES_BLUEPRINT, url_prefix='/places')
APP.register_blueprint(USERS_BLUEPRINT, url_prefix='/users')

# initialize database api
DATABASE = DB.init()

APP.json_encoder = CustomJSONEncoder

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port='5000', debug=True)
