from flask import Flask
from encoders import CustomJSONEncoder
from flask_cors import CORS
from controllers.places_controller import PLACES_BLUEPRINT
from controllers.users_controller import USERS_BLUEPRINT

APP = Flask(__name__)
CORS(APP)

APP.json_encoder = CustomJSONEncoder
APP.register_blueprint(PLACES_BLUEPRINT, url_prefix='/places')
APP.register_blueprint(USERS_BLUEPRINT, url_prefix='/users')

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port='5000', debug=True)
