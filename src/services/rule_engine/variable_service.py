from models.rule import RuleCondition


class Variable:
    def __init__(self, order):
        self.order = order


class DeliveryReputationVariable(Variable):
    @property
    def value(self):
        return self.order.delivery.reputation


class UserReputationVariable(Variable):
    @property
    def value(self):
        return self.order.owner.reputation


class ConditionVariableService:
    variable_mapping = {
        RuleCondition.USER_REPUTATION: UserReputationVariable,
        RuleCondition.DELIVERY_REPUTATION: DeliveryReputationVariable
    }

    def get_value(self, order, variable):
        return self.variable_mapping[variable](order).value
