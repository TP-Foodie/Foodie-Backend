from mongoengine import Document, fields, EmbeddedDocument


class RuleCondition(EmbeddedDocument):
    UserReputation = 'UR'
    UserDailyTravels = 'UDT'
    UserMonthlyTravels = 'UMT'
    UserAntiquity = 'UA'
    DeliveryReputation = 'DR'
    DeliveryDailyTravels = 'DDT'
    DeliveryMonthlyTravels = 'DMT'
    DeliveryAntiquity = 'DA'
    DeliveryBalance = 'DB'
    CashPaymentMethod = 'CPM'
    CreditPaymentMethod = 'CRPM'
    OrderDuration = 'OD'
    OrderDistance = 'ODI'
    OrderPosition = 'OP'
    OrderDate = 'ODA'
    OrdersQuantity = 'OC'
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
        OrderDate,
        OrdersQuantity,
        TravelDay,
    )

    GreaterThanEqual = 'GTE'
    GreaterThan = 'GT'
    LessThan = 'LT'
    LessThanEqual = 'LTE'
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
    condition_value = fields.StringField(max_length=100)


class RuleConsequence(EmbeddedDocument):
    PERCENTAGE = 'P'
    VALUE = 'V'

    CONSEQUENCE_TYPES = (PERCENTAGE, VALUE)

    consequence_type = fields.StringField(max_length=10, choices=CONSEQUENCE_TYPES)
    value = fields.StringField(max_length=100)


class Rule(Document):
    name = fields.StringField(max_length=100)
    consequence = fields.EmbeddedDocumentField(RuleConsequence)
    condition = fields.EmbeddedDocumentField(RuleCondition)
    value = fields.StringField(max_length=100)
