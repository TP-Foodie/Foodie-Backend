from src.models.rule import Rule


class RuleRepository:
    def create(self, name, condition, consequence):
        return Rule.objects.create(
            name=name,
            condition=condition,
            consequence=consequence
        )
