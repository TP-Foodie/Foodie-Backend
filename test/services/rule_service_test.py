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

from src.models.rule import RuleCondition, Rule, RuleConsequence
from src.services.exceptions.rule_exception import MissingArgumentsException
from src.services.rule_service import RuleService


@pytest.mark.usefixtures('a_client')
class TestRuleService:
    rule_service = RuleService()

    def test_create_rule_with_no_consequence_should_create_one(self):
        self.rule_service.create(
            variable=RuleCondition.DeliveryReputation,
            operator=RuleCondition.GreaterThan,
            condition_value=1
        )

        assert Rule.objects.count() == 1

    def test_create_rule_with_consequence(self):
        self.rule_service.create(
            variable=RuleCondition.OrderDate,
            operator=RuleCondition.IsTrue,
            condition_value='wednesday',
            consequence_type=RuleConsequence.PERCENTAGE,
            consequence_value=5,
        )

        assert Rule.objects.count() == 1

    def test_create_rule_without_variable_should_right_exception(self):
        with pytest.raises(MissingArgumentsException):
            self.rule_service.create(
                operator=RuleCondition.IsTrue,
                condition_value='wednesday',
                consequence_type=RuleConsequence.PERCENTAGE,
                consequence_value=5
            )
