from models.rule import RuleCondition


class GreaterThanOperator:
    def apply(self, first_value, second_value):
        return first_value > second_value


class GreaterThanEqualOperator:
    def apply(self, first_value, second_value):
        return first_value >= second_value


class LessThanOperator:
    def apply(self, first_value, second_value):
        return first_value < second_value


class LessThanEqualOperator:
    def apply(self, first_value, second_value):
        return first_value <= second_value


class IsEqualOperator:
    def apply(self, first_value, second_value):
        return first_value == second_value


class ConditionOperatorService:
    OPERATORS_MAPPING = {
        RuleCondition.GREATER_THAN: GreaterThanOperator,
        RuleCondition.GREATER_THAN_EQUAL: GreaterThanEqualOperator,
        RuleCondition.LESS_THAN: LessThanOperator,
        RuleCondition.LESS_THAN_EQUAL: LessThanEqualOperator,
        RuleCondition.IS: IsEqualOperator,
    }

    def apply(self, operator, first_value, second_value):
        return self.OPERATORS_MAPPING[operator]().apply(first_value, second_value)
