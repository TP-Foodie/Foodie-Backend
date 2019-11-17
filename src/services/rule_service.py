from copy import deepcopy

from models.rule import RuleCondition, RuleConsequence
from repositories.rule_history_repository import RuleHistoryRepository
from repositories.rule_repository import RuleRepository
from repositories import order_repository
from schemas.rule_schema import CreateRuleSchema
from services import user_service
from services.rule_engine.condition_service import RuleConditionService
from services.rule_engine.consequence_service import RuleConsequenceService


class RuleService:
    rule_repository = RuleRepository()
    rule_history_repository = RuleHistoryRepository()
    create_schema = CreateRuleSchema()
    condition_service = RuleConditionService()
    consequence_service = RuleConsequenceService()

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
        new_rule = self.rule_repository.create(data)
        self.rule_history_repository.create(new_rule.id)

        return new_rule

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
        duplicated['original'] = False
        return self.rule_repository.create(duplicated)

    def add_to_history(self, rule_id):
        history = self.rule_history_repository.get_for(rule_id)
        duplicated = self.duplicate(rule_id)

        history.versions.append(duplicated.id)
        history.save()

    def history(self, rule_id):
        return self.rule_history_repository.get_for(rule_id)

    def quote_price(self, order_id):
        order = order_repository.get_order(order_id)
        total = 0
        rules_to_apply = self.rule_repository.active_sorted_by_value()\
            .filter(benefit=user_service.is_premium(order.owner))

        for rule in rules_to_apply:
            result = self.condition_service.apply(order, *rule.conditions)
            if result:
                total = self.consequence_service.apply(rule.consequence, total, order)
        return total

    def benefits(self):
        return self.rule_repository.all().filter(benefit=True)
