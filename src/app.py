"""This module initiates Flask APP."""

import os
from flask import Flask

from repositories.database_api import DB
from deliveries_disponibles.controllers.deliveries_disponibles_controller import (
    DELIVERIES_DISPONIBLES_BLUEPRINT)
from deliveries_disponibles.exception_handlers import (
    DELIVERIES_DISPONIBLES_EXCEPTIONS_HANDLER)

# initialize Flask app
APP = Flask(__name__)

# set default api VERSION to v1
VERSION = os.environ.get('API_VERSION', 'v1')
PREFIX = f"/api/{VERSION}"

# register Flask blueprints
APP.register_blueprint(DELIVERIES_DISPONIBLES_BLUEPRINT, url_prefix=f'{PREFIX}/')
APP.register_blueprint(DELIVERIES_DISPONIBLES_EXCEPTIONS_HANDLER)

# initialize database api
DATABASE = DB.init()

if __name__ == "__main__":
    APP.run(host='0.0.0.0', port='5000', debug=True)
