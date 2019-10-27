from unittest.mock import patch

from models.rule import RuleConsequence, RuleCondition
from services.rule_engine.consequence_service import RuleConsequenceService


class TestRuleConsequenceService:
    consequence_service = RuleConsequenceService()

    def test_apply_with_positive_value_adds_it(self):
        consequence = RuleConsequence(consequence_type=RuleConsequence.VALUE, value=1)
        result = self.consequence_service.apply(consequence, 10)

        assert result == 11

    def test_apply_with_negative_value_should_reduce_it(self):
        consequence = RuleConsequence(consequence_type=RuleConsequence.VALUE, value=-1)
        result = self.consequence_service.apply(consequence, 10)

        assert result == 9

    def test_apply_with_percentage_should_add_right_value(self):
        consequence = RuleConsequence(consequence_type=RuleConsequence.PERCENTAGE, value=10)
        result = self.consequence_service.apply(consequence, 10)

        assert result == 11.0

    def test_apply_with_percentage_and_negative_value_should_reduce(self):
        consequence = RuleConsequence(consequence_type=RuleConsequence.PERCENTAGE, value=-10)
        result = self.consequence_service.apply(consequence, 10)

        assert result == 9.0

    @patch('services.rule_engine.consequence_service.ConditionVariableService.get_value')
    def test_apply_with_value_per_unit_should_multiple_value_by_condition_variable(self,
                                                                                   mocked_distance,
                                                                                   a_client,
                                                                                   an_order):
        # pylint: disable=unused-argument
        mocked_distance.return_value = 10
        consequence = RuleConsequence(consequence_type=RuleConsequence.PER_UNIT_VALUE,
                                      value=-10,
                                      variable=RuleCondition.ORDER_DISTANCE)
        result = self.consequence_service.apply(consequence, 200, an_order)

        assert result == 100
