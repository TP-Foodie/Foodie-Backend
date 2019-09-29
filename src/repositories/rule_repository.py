from src.models.rule import Rule
from src.schemas.rule_schema import ListRuleSchema


class RuleRepository:
    list_repository = ListRuleSchema(many=True)

    def create(self, name, condition, consequence):
        return Rule.objects.create(
            name=name,
            condition=condition,
            consequence=consequence
        )

    def list(self):
        return self.list_repository.dump(Rule.objects.all())
