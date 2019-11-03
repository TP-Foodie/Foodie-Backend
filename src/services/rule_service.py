from copy import deepcopy

from models.rule import RuleCondition, RuleConsequence
from repositories.rule_history_repository import RuleHistoryRepository
from repositories.rule_repository import RuleRepository
from schemas.rule_schema import CreateRuleSchema


class RuleService:
    rule_repository = RuleRepository()
    rule_history_repository = RuleHistoryRepository()
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
        self.add_to_history(rule_id)
        return self.rule_repository.update(rule_id, new_fields)

    def delete(self, rule_id):
        return self.rule_repository.delete(rule_id)

    def duplicate(self, rule_id):
        duplicated = deepcopy(self.get(rule_id))
        duplicated['id'] = None
        return self.rule_repository.create(duplicated)

    def add_to_history(self, rule_id):
        history = self.rule_history_repository.get_for(rule_id)
        duplicated = self.duplicate(rule_id)

        if not history:
            self.rule_history_repository.create(rule_id, duplicated.id)
        else:
            history.versions.append(duplicated.id)
            history.save()

    def history(self, rule_id):
        return self.rule_history_repository.get_for(rule_id)
