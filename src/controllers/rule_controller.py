from flask import Blueprint, jsonify, request

from src.controllers.parser import parse_rule_request
from src.controllers.utils import HTTP_200_OK, HTTP_201_CREATED, NO_CONTENT
from src.services.auth_service import authenticate
from src.services.rule_service import RuleService

RULES_BLUEPRINT = Blueprint('rules', __name__)


rule_service = RuleService()


@RULES_BLUEPRINT.route('/', methods=['GET'])
@authenticate
def list_rules():
    data = jsonify(rule_service.list())
    return data, HTTP_200_OK


@RULES_BLUEPRINT.route('/<rule_id>', methods=['GET'])
@authenticate
def get_rule(rule_id):
    data = jsonify(rule_service.get(rule_id))
    return data, HTTP_200_OK


@RULES_BLUEPRINT.route('/', methods=['POST'])
@authenticate
def create_rule():
    rule_service.create(**parse_rule_request(request.json))
    return NO_CONTENT, HTTP_201_CREATED
