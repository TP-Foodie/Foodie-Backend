from src.models.rule import RuleCondition
from src.services.rule_engine.condition_service import RuleConditionService


class TestRuleConditionService:
    condition_service = RuleConditionService()

    def test_apply_to_empty_array_returns_true(self, an_order):
        assert not self.condition_service.apply(an_order, [])

    def test_apply_with_user_reputation(self, an_order):
        condition = RuleCondition(
            variable=RuleCondition.USER_REPUTATION,
            operator=RuleCondition.GREATER_THAN,
            condition_value=2
        )

        an_order.owner.reputation = 3

        assert self.condition_service.apply(an_order, condition)
