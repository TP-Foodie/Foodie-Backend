from flask import Flask
from encoders import CustomJSONEncoder
from controllers.places_controller import places_blueprint
from controllers.users_controller import users_blueprint

APP = Flask(__name__)

APP.json_encoder = CustomJSONEncoder
APP.register_blueprint(places_blueprint, url_prefix='/places')
APP.register_blueprint(users_blueprint, url_prefix='/users')

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port='5000', debug=True)
