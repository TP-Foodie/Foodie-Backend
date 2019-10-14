from models.rule import RuleCondition


class GreaterThanOperator:
    def apply(self, first_value, second_value):
        return first_value > second_value


class LessThanOperator:
    def apply(self, first_value, second_value):
        return first_value < second_value


class ConditionOperatorService:
    OPERATORS_MAPPING = {
        RuleCondition.GREATER_THAN: GreaterThanOperator,
        RuleCondition.LESS_THAN: LessThanOperator
    }

    def apply(self, operator, first_value, second_value):
        return self.OPERATORS_MAPPING[operator]().apply(first_value, second_value)
