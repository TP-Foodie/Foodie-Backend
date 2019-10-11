from models.rule import RuleCondition, RuleConsequence
from repositories.rule_repository import RuleRepository
from schemas.rule_schema import CreateRuleSchema


class RuleService:
    rule_repository = RuleRepository()
    create_schema = CreateRuleSchema()

    @property
    def variables(self):
        return RuleCondition.VARIABLES

    @property
    def operators(self):
        return RuleCondition.OPERATORS

    @property
    def consequence_types(self):
        return RuleConsequence.CONSEQUENCE_TYPES

    def create(self, **kwargs):
        data = self.create_schema.load(kwargs)
        return self.rule_repository.create(data)

    def list(self):
        return self.rule_repository.list()

    def get(self, rule_id):
        return self.rule_repository.get(rule_id)

    def update(self, rule_id, new_fields):
        return self.rule_repository.update(rule_id, new_fields)
