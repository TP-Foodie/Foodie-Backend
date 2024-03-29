from models.rule import Rule
from schemas.rule_schema import ListRuleSchema, RuleSchema


class RuleRepository:
    rules_schema = ListRuleSchema(many=True)
    rule_schema = RuleSchema()

    def create(self, data):
        return Rule.objects.create(**data)

    def list(self):
        return self.rules_schema.dump(self.all().filter(benefit=False))

    def all(self):
        return Rule.objects.filter(original=True)

    def get(self, rule_id):
        return self.rule_schema.dump(Rule.objects.get(id=rule_id))

    def get_raw(self, rule_id):
        return Rule.objects.get(id=rule_id)

    def conditions(self, rule_id):
        return Rule.objects.get(id=rule_id).conditions

    def update(self, rule_id, new_data):
        Rule.objects.get(id=rule_id).update(**new_data)
        return self.get(rule_id)

    def delete(self, rule_id):
        return Rule.objects.get(id=rule_id).delete()

    def active_sorted_by_value(self):
        return self.all().filter(active=True).order_by('-consequence__consequence_type')
