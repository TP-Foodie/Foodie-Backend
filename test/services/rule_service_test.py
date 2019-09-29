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
#     }
# }
import pytest

from src.models.rule import RuleCondition, Rule
from src.services.RuleService import RuleService


@pytest.mark.usefixtures('a_client')
class TestRuleService:
    rule_service = RuleService()

    def test_create_rule_with_condition_delivery_reputation_greater_than_1(self):
        self.rule_service.create(
            variable=RuleCondition.DeliveryReputation,
            operator=RuleCondition.GreaterThan,
            condition_value=1
        )

        assert Rule.objects.count() == 1
