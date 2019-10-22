from datetime import datetime
from services.rule_engine.operator_service import ConditionOperatorService
from services.rule_engine.variable_service import ConditionVariableService
from models.rule import RuleCondition


class RuleConditionService:
    DEFAULT_DATE_FORMAT = "%a, %d %b %Y %H:%M:%S %Z"
    DATE_VARIABLES = [RuleCondition.ORDER_DATE]
    TIME_VARIABLES = [RuleCondition.ORDER_TIME]

    variable_service = ConditionVariableService()
    operator_service = ConditionOperatorService()

    def apply(self, order, *conditions):
        for condition in conditions:
            variable_value = self.variable_service.get_value(order, condition.variable)
            condition_value = self.parse_value(condition.variable, condition.condition_value)
            result = self.operator_service.apply(condition.operator, variable_value, condition_value)
            if not result:
                return False
        return True

    def parse_value(self, variable, value):
        if variable not in self.DATE_VARIABLES and variable not in self.TIME_VARIABLES:
            return int(value)

        date_value = datetime.strptime(value, self.DEFAULT_DATE_FORMAT)

        return date_value.date() if variable in self.DATE_VARIABLES else date_value.time()
