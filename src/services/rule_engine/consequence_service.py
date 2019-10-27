from models.rule import RuleConsequence
from services.rule_engine.variable_service import ConditionVariableService


class ConsequenceType:
    def __init__(self, consequence):
        self.consequence = consequence


class ValueConsequenceType(ConsequenceType):
    def apply(self, value, consequence, _):
        return value + consequence.value


class PercentageConsequenceType(ConsequenceType):
    def to_percentage(self, value):
        return value / 100

    def apply(self, value, consequence, _):
        return value + self.to_percentage(value * consequence.value)


class PerUnitConsequenceType(ConsequenceType):
    variable_service = ConditionVariableService()

    def apply(self, value, consequence, order):
        return value + consequence.value * self.variable_service.get_value(order, self.consequence.variable)


class RuleConsequenceService:
    CONSEQUENCE_TYPE_MAPPING = {
        RuleConsequence.VALUE: ValueConsequenceType,
        RuleConsequence.PERCENTAGE: PercentageConsequenceType,
        RuleConsequence.PER_UNIT_VALUE: PerUnitConsequenceType,
    }

    def apply(self, consequence, value, order=None):
        return self.CONSEQUENCE_TYPE_MAPPING[consequence.consequence_type](consequence).apply(value, consequence, order)
