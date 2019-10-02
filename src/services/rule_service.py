from src.repositories.rule_repository import RuleRepository
from src.schemas.rule_schema import CreateRuleSchema


class RuleService:
    CONDITION_ARGUMENTS = ['variable', 'operator', 'condition_value']
    CONSEQUENCE_ARGUMENTS = ['consequence_type', 'value']

    rule_repository = RuleRepository()
    create_schema = CreateRuleSchema()

    def create(self, **kwargs):
        data = self.create_schema.load(kwargs)
        return self.rule_repository.create(data)

    def list(self):
        return self.rule_repository.list()

    def get(self, rule_id):
        return self.rule_repository.get(rule_id)

    def update(self, rule_id, new_fields):
        pass

    #  TODO: delegate create and update validation to marashmallow
