from src.models.rule import Rule
from src.schemas.rule_schema import ListRuleSchema, RuleSchema


class RuleRepository:
    rules_schema = ListRuleSchema(many=True)
    rule_schema = RuleSchema()

    def create(self, data):
        return Rule.objects.create(**data)

    def list(self):
        return self.rules_schema.dump(Rule.objects.all())

    def get(self, rule_id):
        return self.rule_schema.dump(Rule.objects.get(id=rule_id))
