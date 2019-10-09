from flask import Blueprint, jsonify, request

from src.controllers.utils import HTTP_200_OK, HTTP_201_CREATED
from src.services.auth_service import authenticate
from src.services.rule_service import RuleService

RULES_BLUEPRINT = Blueprint('rules', __name__)

MISSING_ARGS_ERROR_MESSAGE = "missing arguments"

rule_service = RuleService()  # pylint: disable=invalid-name


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
    new_rule = rule_service.create(**request.json)
    return jsonify(new_rule), HTTP_201_CREATED


@RULES_BLUEPRINT.route('/<rule_id>', methods=['PATCH'])
@authenticate
def update_rule(rule_id):
    updated = rule_service.update(rule_id, request.json)
    return jsonify(updated), HTTP_200_OK


@RULES_BLUEPRINT.route('/variables/', methods=['GET'])
@authenticate
def get_variables():
    return jsonify(rule_service.variables), HTTP_200_OK


@RULES_BLUEPRINT.route('/operators/', methods=['GET'])
@authenticate
def get_operators():
    return jsonify(rule_service.operators), HTTP_200_OK


@RULES_BLUEPRINT.route('/consequence_types/', methods=['GET'])
@authenticate
def get_consequence_types():
    return jsonify(rule_service.consequence_types), HTTP_200_OK
