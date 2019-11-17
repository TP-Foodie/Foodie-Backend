from flask import Blueprint

from logger import log_request_response
from services.auth_service import authenticate

USER_RATING_BLUEPRINT = Blueprint('user_ratings', __name__)


@USER_RATING_BLUEPRINT.route('/', methods=['POST'])
@log_request_response
@authenticate
def create():
    return ''
