from models.rule import RuleCondition, RuleConsequence
from repositories.rule_repository import RuleRepository
from schemas.rule_schema import CreateRuleSchema
from repositories import order_repository
from services.rule_engine.condition_service import RuleConditionService
from services.rule_engine.consequence_service import RuleConsequenceService


class RuleService:
    rule_repository = RuleRepository()
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
        return self.rule_repository.create(data)

    def list(self):
        return self.rule_repository.list()

    def get(self, rule_id):
        return self.rule_repository.get(rule_id)

    def update(self, rule_id, new_fields):
        return self.rule_repository.update(rule_id, new_fields)

    def delete(self, rule_id):
        return self.rule_repository.delete(rule_id)

    def quote_price(self, order_id):
        order = order_repository.get_order(order_id)
        total = 0
        for rule in self.rule_repository.sorted_by_value():
            result = self.condition_service.apply(order, *rule.conditions)
            if result:
                total = self.consequence_service.apply(rule.consequence, total, order)
        return total
