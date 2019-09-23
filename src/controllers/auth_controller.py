from flask import Blueprint

AUTH_BLUEPRINT = Blueprint('auth', __name__)


@AUTH_BLUEPRINT.route('/', methods=['POST'])
def post():
    return
