"""This module initiates Flask APP."""

from flask import Flask
from flask_cors import CORS
from mongoengine import connect
from flask_swagger_ui import get_swaggerui_blueprint
import firebase_admin
from firebase_admin import credentials

from controllers.statistics_controller import STATISTICS_BLUEPRINT
from encoders import CustomJSONEncoder
from settings import Config

from controllers.auth_controller import AUTH_BLUEPRINT
from controllers.place_controller import PLACES_BLUEPRINT
from controllers.user_controller import USERS_BLUEPRINT
from controllers.available_deliveries_controller import AVAILABLE_DELIVERIES_BLUEPRINT
from controllers.order_controller import ORDERS_BLUEPRINT
from controllers.rule_controller import RULES_BLUEPRINT
from controllers.chat_controller import CHATS_BLUEPRINT
from controllers.user_rating_controller import USER_RATING_BLUEPRINT
from error_handlers import ERRORS_BLUEPRINT

# initialize Flask app
APP = Flask(__name__)
CORS(APP)
CRED = credentials.Certificate(Config.GOOGLE_APPLICATION_CREDENTIALS)
firebase_admin.initialize_app(CRED)

SWAGGER_UI_BLUEPRINT = get_swaggerui_blueprint(
    "/swagger",
    "/static/swagger.yml",
    config={
        'app_name': "Foodie"
    }
)

# set default api VERSION to v1
PREFIX = "/api/v1"

# register Flask blueprints
APP.register_blueprint(AUTH_BLUEPRINT, url_prefix=f'{PREFIX}/auth')
APP.register_blueprint(AVAILABLE_DELIVERIES_BLUEPRINT, url_prefix=f'{PREFIX}/')
APP.register_blueprint(ORDERS_BLUEPRINT, url_prefix=f'{PREFIX}/orders')
APP.register_blueprint(PLACES_BLUEPRINT, url_prefix=f'{PREFIX}/places')
APP.register_blueprint(USERS_BLUEPRINT, url_prefix=f'{PREFIX}/users')
APP.register_blueprint(RULES_BLUEPRINT, url_prefix=f'{PREFIX}/rules')
APP.register_blueprint(CHATS_BLUEPRINT, url_prefix=f'{PREFIX}/chats')
APP.register_blueprint(STATISTICS_BLUEPRINT, url_prefix=f'{PREFIX}/statistics')
APP.register_blueprint(USER_RATING_BLUEPRINT, url_prefix=f'{PREFIX}/user_ratings')

APP.register_blueprint(ERRORS_BLUEPRINT)

APP.register_blueprint(SWAGGER_UI_BLUEPRINT, url_prefix="/swagger")

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
