from src.models.rule import RuleCondition
from src.services.rule_engine.operator_service import ConditionOperatorService


class TestOperatorService:
    operator_service = ConditionOperatorService()

    def test_apply_greater_than_returns_true_if_its_greater(self):
        assert self.operator_service.apply(RuleCondition.GREATER_THAN, 5, 3)

    def test_apply_greater_than_retunrs_false_if_its_smaller(self):
        assert not self.operator_service.apply(RuleCondition.GREATER_THAN, 1, 3)

    def test_apply_greater_than_returns_false_if_are_equal(self):
        assert not self.operator_service.apply(RuleCondition.GREATER_THAN, 1, 1)
