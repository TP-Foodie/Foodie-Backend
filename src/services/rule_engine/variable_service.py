from models.rule import RuleCondition

from services import user_service


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


class UserDailyTravelsVariable(Variable):
    @property
    def value(self):
        return user_service.daily_travels(self.order.owner)


class DeliveryDailyTravelsVariable(Variable):
    @property
    def value(self):
        return user_service.daily_travels(self.order.delivery)


class ConditionVariableService:
    variable_mapping = {
        RuleCondition.USER_REPUTATION: UserReputationVariable,
        RuleCondition.DELIVERY_REPUTATION: DeliveryReputationVariable,
        RuleCondition.USER_DAILY_TRAVELS: DeliveryReputationVariable,
        RuleCondition.DELIVERY_DAILY_TRAVELS: DeliveryDailyTravelsVariable,
    }

    def get_value(self, order, variable):
        return self.variable_mapping[variable](order).value
