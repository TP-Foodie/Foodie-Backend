from models.rule import RuleConsequence
from services.rule_engine.consequence_service import RuleConsequenceService


class TestRuleConsequenceService:
    consequence_service = RuleConsequenceService()

    def test_apply_with_positive_value_adds_it(self):
        result = self.consequence_service.apply(RuleConsequence.VALUE, 10, 1)
        assert result == 11

    def test_apply_with_negative_value_should_reduce_it(self):
        result = self.consequence_service.apply(RuleConsequence.VALUE, 10, -1)
        assert result == 9

    def test_apply_with_percentage_should_add_right_value(self):
        result = self.consequence_service.apply(RuleConsequence.PERCENTAGE, 10, 10)
        assert result == 11.0

    def test_apply_with_percentage_and_negative_value_should_reduce(self):
        result = self.consequence_service.apply(RuleConsequence.PERCENTAGE, 10, -10)
        assert result == 9.0
