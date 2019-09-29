from mongoengine import Document, fields


class RuleCondition(Document):
    UserReputation = 'UR'
    UserDailyTravels = 'UDT'
    UserMonthlyTravels = 'UMT'
    UserAntiquity = 'UA'
    DeliveryReputation = 'DR'
    DeliveryDailyTravels = 'DDT',
    DeliveryMonthlyTravels = 'DMT',
    DeliveryAntiquity = 'DA',
    DeliveryBalance = 'DB',
    CashPaymentMethod = 'CPM',
    CreditPaymentMethod = 'CRPM'
    OrderDuration = 'OD',
    OrderDistance = 'ODI',
    OrderPosition = 'OP',
    OrderTime = 'OT',
    OrdersQuantity = 'OC',
    TravelDay = 'TD'

    VARIABLES = (
        UserReputation,
        UserDailyTravels,
        UserMonthlyTravels,
        UserAntiquity,
        DeliveryReputation,
        DeliveryDailyTravels,
        DeliveryMonthlyTravels,
        DeliveryAntiquity,
        DeliveryBalance,
        CashPaymentMethod,
        CreditPaymentMethod,
        OrderDuration,
        OrderDistance,
        OrderPosition,
        OrderTime,
        OrdersQuantity,
        TravelDay,
    )

    GreaterThanEqual = 'GTE'
    GreaterThan = 'GT',
    LessThan = 'LT',
    LessThanEqual = 'LTE',
    IsTrue = 'IT'

    OPERATORS = (
        GreaterThanEqual,
        GreaterThan,
        LessThan,
        LessThanEqual,
        IsTrue
    )

    variable = fields.StringField(max_length=10, choices=VARIABLES)
    operator = fields.StringField(max_length=10, choices=OPERATORS)
