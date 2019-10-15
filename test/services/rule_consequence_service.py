from models.rule import RuleConsequence
from services.rule_engine.consequence_service import RuleConsequenceService


class TestRuleConsequenceService:
    consequence_service = RuleConsequenceService()

    def test_apply_with_positive_value_adds_it(self):
        result = self.consequence_service.apply(RuleConsequence.VALUE, 10, 1)
        assert result == 9
