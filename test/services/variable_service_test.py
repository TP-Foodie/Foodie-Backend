import pytest
from models.rule import RuleCondition
from services.rule_engine.variable_service import ConditionVariableService


@pytest.mark.usefixtures('a_client')
class TestVariableService:
    variable_service = ConditionVariableService()

    def test_get_value_for_user_reputation(self, an_order):
        value = self.variable_service.get_value(an_order, RuleCondition.USER_REPUTATION)

        assert value == an_order.owner.reputation
