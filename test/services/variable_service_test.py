from unittest.mock import patch

from datetime import datetime
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

    def test_get_value_for_user_antiquity(self, an_order):
        value = self.variable_service.get_value(an_order, RuleCondition.USER_ANTIQUITY)

        assert value == user_service.antiquity(an_order.owner)

    def test_get_value_for_user_balance(self, an_order):
        an_order.owner.balance = 3
        value = self.variable_service.get_value(an_order, RuleCondition.USER_BALANCE)

        assert value == 3

    def test_get_value_for_payment_method(self, an_order):
        an_order.payment_method = RuleCondition.CREDIT_PAYMENT_METHOD
        value = self.variable_service.get_value(an_order, RuleCondition.PAYMENT_METHOD)

        assert value == RuleCondition.CREDIT_PAYMENT_METHOD

    def test_get_value_for_non_existing_variable_returns_zero(self, an_order):
        value = self.variable_service.get_value(an_order, 'NON_EXISTING')

        assert value == 0

    def test_get_value_for_order_date(self, an_order):
        an_order.date = datetime.now()
        value = self.variable_service.get_value(an_order, RuleCondition.ORDER_DATE)

        assert value == datetime.now().date()

    def test_get_value_for_order_time(self, an_order):
        now = datetime.now()
        an_order.date = now
        value = self.variable_service.get_value(an_order, RuleCondition.ORDER_TIME)

        assert value == now.time()

    def test_get_value_for_order_distance(self, an_order):
        with patch('services.order_service.distance') as mocked_distance:
            mocked_distance.return_value = 2
            value = self.variable_service.get_value(an_order, RuleCondition.ORDER_DISTANCE)

        assert value == 2

    def test_get_value_for_order_count(self, an_order_factory):
        an_order = an_order_factory()
        an_order_factory()

        value = self.variable_service.get_value(an_order, RuleCondition.ORDER_QUANTITY)

        assert value == 2

    def test_get_value_for_order_position_return_city(self, an_order):
        with patch('services.order_service.order_position') as mocked_position:
            mocked_position.return_value = "Escobar"
            value = self.variable_service.get_value(an_order, RuleCondition.ORDER_POSITION)

        assert value == "Escobar"

    def test_get_value_for_order_day_returns_day_number(self, an_order):
        an_order.date = datetime.strptime('Wed, 27 Nov 2019 15:30:00 GMT',
                                          "%a, %d %b %Y %H:%M:%S %Z")
        an_order.save()

        value = self.variable_service.get_value(an_order, RuleCondition.ORDER_DAY)

        assert value == 3
