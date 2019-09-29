from flask import Blueprint

from src.controllers.utils import NO_CONTENT, HTTP_403_UNAUTHORIZED

RULES_BLUEPRINT = Blueprint('rules', __name__)


@RULES_BLUEPRINT.route('/', methods=['GET'])
def list_rules():
    return NO_CONTENT, HTTP_403_UNAUTHORIZED
