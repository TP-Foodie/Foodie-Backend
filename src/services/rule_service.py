from src.models.rule import RuleConsequence, RuleCondition
from src.repositories.rule_repository import RuleRepository
from src.services.exceptions.rule_exception import MissingArgumentsException


class RuleService:
    DEFAULT_VALUE = '0'

    rule_repository = RuleRepository()

    def create(self, **kwargs):
        kwargs = self.check_args(kwargs)

        condition = RuleCondition(**{key: str(kwargs[key]) for key in ['variable', 'operator', 'condition_value']})
        consequence = RuleConsequence(**{key: str(kwargs[key]) for key in ['consequence_type', 'value']})

        return self.rule_repository.create(kwargs['name'], condition, consequence)

    def check_args(self, args):
        for arg in ['variable', 'operator']:
            if arg not in args:
                raise MissingArgumentsException()

        self.check_arg(args, 'consequence_type', RuleConsequence.VALUE)
        self.check_arg(args, 'value', self.DEFAULT_VALUE)
        self.check_arg(args, 'condition_value', self.DEFAULT_VALUE)
        self.check_arg(args, 'name', None)

        return args

    def check_arg(self, args, arg_name, default):
        args[arg_name] = args.get(arg_name, default)
        return args
