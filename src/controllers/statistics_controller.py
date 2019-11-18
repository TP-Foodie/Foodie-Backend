from flask import Blueprint

from logger import log_request_response
from services.auth_service import authenticate

STATISTICS_BLUEPRINT = Blueprint('statistics', __name__)


@STATISTICS_BLUEPRINT.route('/registrations', methods=['GET'])
@log_request_response
@authenticate
def registrations():
    return ''
