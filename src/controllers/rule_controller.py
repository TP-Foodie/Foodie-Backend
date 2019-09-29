from flask import Blueprint, jsonify

from src.controllers.utils import HTTP_200_OK
from src.services.auth_service import authenticate
from src.services.rule_service import RuleService

RULES_BLUEPRINT = Blueprint('rules', __name__)


rule_service = RuleService()


@RULES_BLUEPRINT.route('/', methods=['GET'])
@authenticate
def list_rules():
    data = jsonify(rule_service.list())
    return data, HTTP_200_OK
