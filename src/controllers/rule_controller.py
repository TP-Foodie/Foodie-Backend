from flask import Blueprint, jsonify, request

from controllers.utils import HTTP_200_OK, HTTP_201_CREATED, NO_CONTENT
from schemas.rule_schema import RuleHistorySchema
from schemas.rule_schema import RuleSchema
from logger import log_request_response
from services.auth_service import authenticate
from services.rule_service import RuleService

RULES_BLUEPRINT = Blueprint('rules', __name__)

MISSING_ARGS_ERROR_MESSAGE = "missing arguments"

rule_service = RuleService()  # pylint: disable=invalid-name
rules_schema = RuleSchema(many=True)  # pylint: disable=invalid-name
history_schema = RuleHistorySchema()  # pylint: disable=invalid-name


@RULES_BLUEPRINT.route('/', methods=['GET'])
@log_request_response
@authenticate
def list_rules():
    data = jsonify(rule_service.list())
    return data, HTTP_200_OK


@RULES_BLUEPRINT.route('/<rule_id>', methods=['GET'])
@log_request_response
@authenticate
def get_rule(rule_id):
    data = jsonify(rule_service.get(rule_id))
    return data, HTTP_200_OK


@RULES_BLUEPRINT.route('/', methods=['POST'])
@log_request_response
@authenticate
def create_rule():
    new_rule = rule_service.create(**request.json)
    return jsonify(new_rule), HTTP_201_CREATED


@RULES_BLUEPRINT.route('/<rule_id>', methods=['PATCH'])
@log_request_response
@authenticate
def update_rule(rule_id):
    updated = rule_service.update(rule_id, request.json)
    return jsonify(updated), HTTP_200_OK


@RULES_BLUEPRINT.route('/variables/', methods=['GET'])
@log_request_response
@authenticate
def get_variables():
    return jsonify(rule_service.variables), HTTP_200_OK


@RULES_BLUEPRINT.route('/operators/', methods=['GET'])
@log_request_response
@authenticate
def get_operators():
    return jsonify(rule_service.operators), HTTP_200_OK


@RULES_BLUEPRINT.route('/consequence_types/', methods=['GET'])
@log_request_response
@authenticate
def get_consequence_types():
    return jsonify(rule_service.consequence_types), HTTP_200_OK


@RULES_BLUEPRINT.route('/benefits', methods=['GET'])
@log_request_response
@authenticate
def get_benefits():
    return jsonify(rules_schema.dump(rule_service.benefits()))


@RULES_BLUEPRINT.route('/redeemable', methods=['GET'])
@log_request_response
@authenticate
def get_redeemable_benefits():
    return jsonify(rules_schema.dump(rule_service.redeemable()))


@RULES_BLUEPRINT.route('/<rule_id>', methods=['DELETE'])
@log_request_response
@authenticate
def delete_rule(rule_id):
    rule_service.delete(rule_id)
    return NO_CONTENT, HTTP_200_OK


@RULES_BLUEPRINT.route('/<rule_id>/redeem', methods=['POST'])
@log_request_response
@authenticate
def redeem(user, rule_id):
    rule_service.redeem(rule_id, user.id)
    return NO_CONTENT, HTTP_200_OK


@RULES_BLUEPRINT.route('/<rule_id>/history', methods=['GET'])
@log_request_response
@authenticate
def get_rule_history(rule_id):
    data = history_schema.dump(rule_service.history(rule_id))
    return jsonify(data), HTTP_200_OK
