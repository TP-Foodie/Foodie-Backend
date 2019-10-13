from src.services.rule_service import RuleConditionService


class TestRuleConditionService:
    condition_service = RuleConditionService()

    def test_apply_to_empty_array_returns_true(self):
        assert not self.condition_service.apply([])
