from models.rule import RuleConsequence


class ValueConsequenceType:
    def apply(self, value, value_to_apply):
        return value + value_to_apply


class PercentageConsequenceType:
    def to_percentage(self, value):
        return value / 100

    def apply(self, value, value_to_apply):
        return value + self.to_percentage(value * value_to_apply)


class RuleConsequenceService:
    CONSEQUENCE_TYPE_MAPPING = {
        RuleConsequence.VALUE: ValueConsequenceType,
        RuleConsequence.PERCENTAGE: PercentageConsequenceType
    }

    def apply(self, consequence, value):
        return self.CONSEQUENCE_TYPE_MAPPING[consequence.consequence_type]().apply(value, consequence.value)
