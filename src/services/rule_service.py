from src.models.rule import RuleConsequence, RuleCondition
from src.repositories.rule_repository import RuleRepository
from src.services.exceptions.rule_exception import MissingArgumentsException


class RuleService:
    CONDITION_ARGUMENTS = ['variable', 'operator', 'condition_value']
    CONSEQUENCE_ARGUMENTS = ['consequence_type', 'value']

    rule_repository = RuleRepository()

    def create(self, **kwargs):
        for arg in self.CONDITION_ARGUMENTS:
            if arg not in kwargs:
                raise MissingArgumentsException()

        condition = RuleCondition(**{key: str(kwargs[key]) for key in self.CONDITION_ARGUMENTS})
        consequence = RuleConsequence(**{key: kwargs[key] for key in self.CONSEQUENCE_ARGUMENTS if key in kwargs})

        return self.rule_repository.create(kwargs.get('name', ''), condition, consequence)

    def list(self):
        return self.rule_repository.list()

    def get(self, rule_id):
        return self.rule_repository.get(rule_id)

    def update(self, rule_id, new_fields):
        pass

    #  TODO: delegate create and update validation to marashmallow
