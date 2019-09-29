# {
#     'id': 1,
#     'condition': {
#         'id': 1,
#         'variable': 'today',
#         'operator': 'IS',
#         'condition_value': 'miercoles',
#         'condition': {
#             'id': 1,
#             'variable': 'time',
#             'type': 'GTE'
#         }
#     },
#     'consequence': {
#         'id': 1,
#         'type': '',
#         'value': -5
#     },
#     fact: 'jueves'
# }
import pytest

from src.models.rule import RuleCondition, Rule
from src.services.RuleService import RuleService


@pytest.mark.usefixtures('a_client')
class TestRuleService:
    rule_service = RuleService()

    def test_create_rule_should_create_one(self):
        self.rule_service.create(
            variable=RuleCondition.DeliveryReputation,
            operator=RuleCondition.GreaterThan,
            condition_value=1
        )

        assert Rule.objects.count() == 1

    def test_get_value_for_user_reputation_rule_should_return_user_reputation(self, a_client_user, an_order):
        rule = self.rule_service.create(
            variable=RuleCondition.UserReputation,
            operator=RuleCondition.GreaterThan,
            condition_value=3
        )

        value = self.rule_service.get_value_for(rule, an_order)

        assert value == a_client_user.reputation
