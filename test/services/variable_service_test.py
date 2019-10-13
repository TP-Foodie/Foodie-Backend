from src.models.rule import RuleCondition
from src.services.rule_engine.variable_service import ConditionVariableService


class TestVariableService:
    variable_service = ConditionVariableService()

    def test_get_value_for_user_reputation(self, an_order):
        value = self.variable_service.get_value(an_order, RuleCondition.USER_REPUTATION)

        assert value == an_order.owner.reputation
