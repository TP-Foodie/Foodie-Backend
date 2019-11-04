from models.rule import RuleCondition
from services.rule_engine.operator_service import ConditionOperatorService


class TestOperatorService:
    operator_service = ConditionOperatorService()

    def test_apply_greater_than_returns_true_if_its_greater(self):
        assert self.operator_service.apply(RuleCondition.GREATER_THAN, 5, 3)

    def test_apply_greater_than_retunrs_false_if_its_smaller(self):
        assert not self.operator_service.apply(RuleCondition.GREATER_THAN, 1, 3)

    def test_apply_greater_than_returns_false_if_are_equal(self):
        assert not self.operator_service.apply(RuleCondition.GREATER_THAN, 1, 1)

    def test_apply_less_than_returns_true_if_its_smaller(self):
        assert self.operator_service.apply(RuleCondition.LESS_THAN, 0, 1)

    def test_apply_greater_than_equals_returns_true_if_are_equals(self):
        assert self.operator_service.apply(RuleCondition.GREATER_THAN_EQUAL, 1, 1)

    def test_apply_greater_than_equals_returns_false_if_its_smaller(self):
        assert not self.operator_service.apply(RuleCondition.GREATER_THAN_EQUAL, 0, 1)

    def test_apply_greater_than_equals_returns_true_if_its_greater(self):
        assert self.operator_service.apply(RuleCondition.GREATER_THAN_EQUAL, 2, 1)

    def test_apply_less_than_equal_returns_true_if_are_equal(self):
        assert self.operator_service.apply(RuleCondition.LESS_THAN_EQUAL, 1, 1)

    def test_apply_less_than_equals_returns_false_if_its_bigger(self):
        assert not self.operator_service.apply(RuleCondition.LESS_THAN_EQUAL, 2, 1)

    def test_apply_is_equal_returns_false_if_are_not_equal(self):
        assert not self.operator_service.apply(RuleCondition.IS, 1, 2)

    def test_apply_is_equal_returns_true_if_are_equal(self):
        assert self.operator_service.apply(RuleCondition.IS, 1, 1)
