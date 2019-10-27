from models.rule import Rule
from schemas.rule_schema import ListRuleSchema, RuleSchema


class RuleRepository:
    rules_schema = ListRuleSchema(many=True)
    rule_schema = RuleSchema()

    def create(self, data):
        return Rule.objects.create(**data)

    def list(self):
        return self.rules_schema.dump(Rule.objects.all())

    def all(self):
        return Rule.objects.all()

    def get(self, rule_id):
        return self.rule_schema.dump(Rule.objects.get(id=rule_id))

    def conditions(self, rule_id):
        return Rule.objects.get(id=rule_id).conditions

    def update(self, rule_id, new_data):
        return Rule(**new_data, id=rule_id).save()

    def delete(self, rule_id):
        return Rule.objects.get(id=rule_id).delete()

    def active_sorted_by_value(self):
        return Rule.objects.filter(active=True).order_by('-consequence__consequence_type')
