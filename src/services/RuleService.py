from src.repositories.rule_repository import RuleRepository


class RuleService:
    rule_repository = RuleRepository()

    def create(self, variable, operator, condition_value):
        self.rule_repository.create(variable, operator, str(condition_value))
