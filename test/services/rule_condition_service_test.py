import pytest

from models.rule import RuleCondition
from services.rule_engine.condition_service import RuleConditionService


@pytest.mark.usefixtures('a_client')
class TestRuleConditionService:
    condition_service = RuleConditionService()

    def test_apply_to_no_conditions_returns_true(self, an_order):
        assert self.condition_service.apply(an_order)

    def test_apply_with_user_reputation(self, an_order):
        condition = RuleCondition(
            variable=RuleCondition.USER_REPUTATION,
            operator=RuleCondition.GREATER_THAN,
            condition_value=2
        )

        an_order.owner.reputation = 3

        assert self.condition_service.apply(an_order, condition)

    def test_parse_value_when_variable_is_time_type(self):
        result = self.condition_service.parse_value(RuleCondition.ORDER_TIME, 'Sat, 30 Nov 2019 18:30:00 GMT')

        with pytest.raises(AttributeError):
            assert result.year

        assert result.hour == 18
        assert result.minute == 30
        assert result.second == 0

    def test_parse_value_when_variable_is_date_type(self):
        result = self.condition_service.parse_value(RuleCondition.ORDER_DATE, 'Sat, 30 Nov 2019 18:30:00 GMT')

        with pytest.raises(AttributeError):
            assert result.hour

        assert result.year == 2019
        assert result.month == 11
        assert result.day == 30

    def test_parse_value_when_variable_is_travel_time_type(self):
        result = self.condition_service.parse_value(RuleCondition.TRAVEL_TIME, 'Sat, 30 Nov 2019 18:30:00 GMT')

        with pytest.raises(AttributeError):
            assert result.year

        assert result.hour == 18
        assert result.minute == 30
        assert result.second == 0

    def test_parse_value_when_variable_is_order_position_should_return_city_lowered(self):
        result = self.condition_service.parse_value(RuleCondition.ORDER_POSITION, 'Escobar')

        assert result == 'escobar'
