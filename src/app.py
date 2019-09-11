from flask import Flask
from encoders import CustomJSONEncoder
from flask_cors import CORS
from mongoengine import connect
from settings import Config

from controllers.place_controller import PLACES_BLUEPRINT
from controllers.user_controller import USERS_BLUEPRINT
from error_handlers import exception_handler

APP = Flask(__name__)
CORS(APP)

APP.json_encoder = CustomJSONEncoder
APP.register_blueprint(PLACES_BLUEPRINT, url_prefix='/places')
APP.register_blueprint(USERS_BLUEPRINT, url_prefix='/users')

for key, value in exception_handler.items():
    APP.register_error_handler(key, value)

connect(db=Config.DATABASE_NAME,
        host=Config.DATABASE_HOST,
        port=Config.DATABASE_PORT,
        username=Config.DATABASE_USERNAME,
        password=Config.DATABASE_PASSWORD,
        ssl=Config.DATABASE_SSL)

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port='5000', debug=True)
