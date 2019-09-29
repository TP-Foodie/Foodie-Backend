from src.models.rule import RuleConsequence, RuleCondition
from src.repositories.rule_repository import RuleRepository
from src.services.exceptions.rule_exception import MissingArgumentsException


class RuleService:
    rule_repository = RuleRepository()

    def create(self, **kwargs):
        kwargs = self.check_args(kwargs)

        condition = RuleCondition(**{key: str(kwargs[key]) for key in ['variable', 'operator', 'condition_value']})
        consequence = RuleConsequence(**{key: str(kwargs[key]) for key in ['consequence_type', 'value']})

        self.rule_repository.create(condition, consequence)

    def check_args(self, args):
        for arg in ['variable', 'operator']:
            if arg not in args:
                raise MissingArgumentsException()

        args['consequence_type'] = args['consequence_type'] if 'consequence_type' in args \
            else RuleConsequence.VALUE
        args['value'] = args['value'] if 'value' in args else '0'
        args['condition_value'] = args['condition_value'] if 'condition_value' in args else '0'
        return args
