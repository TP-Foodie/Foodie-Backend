from datetime import datetime
from services.rule_engine.operator_service import ConditionOperatorService
from services.rule_engine.variable_service import ConditionVariableService


class RuleConditionService:
    DEFAULT_DATE_FORMAT = "%a, %d %b %Y %H:%M:%S %Z"

    variable_service = ConditionVariableService()
    operator_service = ConditionOperatorService()

    def apply(self, order, *conditions):
        for condition in conditions:
            variable_value = self.variable_service.get_value(order, condition.variable)
            condition_value = self.parse_value(condition.condition_value)
            result = self.operator_service.apply(condition.operator, variable_value, condition_value)
            if not result:
                return False
        return True

    def parse_value(self, value):
        try:
            return int(value)
        except ValueError:
            return datetime.strptime(value, self.DEFAULT_DATE_FORMAT)
            # TODO convert to date or time according to variable type
