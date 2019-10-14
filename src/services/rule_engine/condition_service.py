from services.rule_engine.operator_service import ConditionOperatorService
from services.rule_engine.variable_service import ConditionVariableService


class RuleConditionService:
    variable_service = ConditionVariableService()
    operator_service = ConditionOperatorService()

    def apply(self, order, *conditions):
        for condition in conditions:
            value = self.variable_service.get_value(order, condition.variable)
            result = self.operator_service.apply(condition.operator, value, condition.condition_value)
            if not result:
                return False
        return True
