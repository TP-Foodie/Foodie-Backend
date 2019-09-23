"""This module initiates Flask APP."""

from flask import Flask
from flask_cors import CORS
from mongoengine import connect
from encoders import CustomJSONEncoder
from settings import Config

from controllers.place_controller import PLACES_BLUEPRINT
from controllers.user_controller import USERS_BLUEPRINT
from controllers.available_deliveries_controller import AVAILABLE_DELIVERIES_BLUEPRINT
from controllers.auth_controller import AUTH_BLUEPRINT
from error_handlers import ERRORS_BLUEPRINT

# initialize Flask app
APP = Flask(__name__)
CORS(APP)

# register Flask blueprints
APP.register_blueprint(
    AVAILABLE_DELIVERIES_BLUEPRINT,
    url_prefix='/api/v1/deliveries')
APP.register_blueprint(PLACES_BLUEPRINT, url_prefix='/api/v1/places')
APP.register_blueprint(USERS_BLUEPRINT, url_prefix='/api/v1/users')
APP.register_blueprint(AUTH_BLUEPRINT, url_prefix='/api/v1/auth')
APP.register_blueprint(ERRORS_BLUEPRINT)

# initialize Mongo Engine (Database)
connect(db=Config.DATABASE_NAME,
        authentication_source=Config.DATABASE_AUTH_SOURCE,
        host=Config.DATABASE_HOST,
        port=Config.DATABASE_PORT,
        username=Config.DATABASE_USERNAME,
        password=Config.DATABASE_PASSWORD,
        ssl=Config.DATABASE_SSL)

APP.json_encoder = CustomJSONEncoder

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port='5000', debug=True)
