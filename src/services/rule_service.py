from src.models.rule import RuleConsequence, RuleCondition
from src.repositories.rule_repository import RuleRepository


class RuleService:
    rule_repository = RuleRepository()

    def create(self, **kwargs):
        kwargs['consequence_type'] = kwargs['consequence_type'] if 'consequence_type' in kwargs\
            else RuleConsequence.VALUE
        kwargs['value'] = kwargs['value'] if 'value' in kwargs else '0'

        condition = RuleCondition(**{key: str(kwargs[key]) for key in ['variable', 'operator', 'condition_value']})
        consequence = RuleConsequence(**{key: str(kwargs[key]) for key in ['consequence_type', 'value']})

        self.rule_repository.create(condition, consequence)
