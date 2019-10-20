import pytest
from models.rule import RuleCondition
from services.rule_engine.variable_service import ConditionVariableService
from services import user_service


@pytest.mark.usefixtures('a_client')
class TestVariableService:
    variable_service = ConditionVariableService()

    def test_get_value_for_user_reputation(self, an_order):
        value = self.variable_service.get_value(an_order, RuleCondition.USER_REPUTATION)

        assert value == an_order.owner.reputation

    def test_get_value_for_delivery_reputation(self, an_order):
        value = self.variable_service.get_value(an_order, RuleCondition.DELIVERY_REPUTATION)

        assert value == an_order.delivery.reputation

    def test_get_value_for_user_daily_travels(self, an_order):
        value = self.variable_service.get_value(an_order, RuleCondition.USER_DAILY_TRAVELS)

        assert value == user_service.daily_travels(an_order.owner)

    def test_get_value_for_delivery_daily_travels(self, an_order):
        value = self.variable_service.get_value(an_order, RuleCondition.DELIVERY_DAILY_TRAVELS)

        assert value == user_service.daily_travels(an_order.delivery)

    def test_get_value_for_delivery_monthly_travels(self, an_order):
        value = self.variable_service.get_value(an_order, RuleCondition.DELIVERY_MONTHLY_TRAVELS)

        assert value == user_service.monthly_travels(an_order.delivery)

    def test_get_value_for_user_monthly_travels(self, an_order):
        value = self.variable_service.get_value(an_order, RuleCondition.USER_MONTHLY_TRAVELS)

        assert value == user_service.monthly_travels(an_order.owner)
