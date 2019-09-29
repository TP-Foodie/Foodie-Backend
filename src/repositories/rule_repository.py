from src.models.rule import Rule, RuleCondition


class RuleRepository:
    def create(self, variable, operator, condition_value):
        return Rule.objects.create(
            condition=RuleCondition(variable=variable, operator=operator, condition_value=condition_value)
        )
