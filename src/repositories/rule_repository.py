from src.models.rule import Rule, RuleCondition, RuleConsequence


class RuleRepository:
    def create(self, condition, consequence):
        return Rule.objects.create(
            condition=condition,
            consequence=consequence
        )
