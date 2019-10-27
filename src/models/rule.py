from mongoengine import Document, fields, EmbeddedDocument


class RuleCondition(EmbeddedDocument):
    USER_REPUTATION = 'UR'
    USER_DAILY_TRAVELS = 'UDT'
    USER_MONTHLY_TRAVELS = 'UMT'
    USER_ANTIQUITY = 'UA'
    DELIVERY_REPUTATION = 'DR'
    DELIVERY_DAILY_TRAVELS = 'DDT'
    DELIVERY_MONTHLY_TRAVELS = 'DMT'
    DELIVERY_ANTIQUITY = 'DA'
    USER_BALANCE = 'DB'
    CASH_PAYMENT_METHOD = 'CPM'
    CREDIT_PAYMENT_METHOD = 'CRPM'
    ORDER_DURATION = 'OD'
    ORDER_DISTANCE = 'ODI'
    ORDER_POSITION = 'OP'
    ORDER_DATE = 'ODA'
    ORDER_TIME = 'OT'
    ORDER_QUANTITY = 'OC'
    TRAVEL_DAY = 'TD'
    TRAVEL_TIME = 'TT'
    PAYMENT_METHOD = 'PM'

    VARIABLES = (
        USER_REPUTATION,
        USER_DAILY_TRAVELS,
        USER_MONTHLY_TRAVELS,
        USER_ANTIQUITY,
        DELIVERY_REPUTATION,
        DELIVERY_DAILY_TRAVELS,
        DELIVERY_MONTHLY_TRAVELS,
        DELIVERY_ANTIQUITY,
        USER_BALANCE,
        PAYMENT_METHOD,
        ORDER_DURATION,
        ORDER_DISTANCE,
        ORDER_POSITION,
        ORDER_DATE,
        ORDER_TIME,
        ORDER_QUANTITY,
        TRAVEL_DAY,
        TRAVEL_TIME
    )

    GREATER_THAN_EQUAL = 'GTE'
    GREATER_THAN = 'GT'
    LESS_THAN = 'LT'
    LESS_THAN_EQUAL = 'LTE'
    IS = 'IT'

    OPERATORS = (
        GREATER_THAN_EQUAL,
        GREATER_THAN,
        LESS_THAN,
        LESS_THAN_EQUAL,
        IS
    )

    PAYMENT_METHODS = (
        CASH_PAYMENT_METHOD,
        CREDIT_PAYMENT_METHOD
    )

    variable = fields.StringField(max_length=10, choices=VARIABLES)
    operator = fields.StringField(max_length=10, choices=OPERATORS)
    condition_value = fields.StringField(max_length=100)


class RuleConsequence(EmbeddedDocument):
    PERCENTAGE = 'P'
    VALUE = 'V'
    PER_UNIT_VALUE = 'PV'

    CONSEQUENCE_TYPES = (PERCENTAGE, VALUE, PER_UNIT_VALUE)

    consequence_type = fields.StringField(max_length=10, choices=CONSEQUENCE_TYPES, default=VALUE)
    value = fields.IntField(max_length=100, default=0)
    variable = fields.StringField(max_length=10, choices=RuleCondition.VARIABLES)


class Rule(Document):
    name = fields.StringField(max_length=100, default=None)
    consequence = fields.EmbeddedDocumentField(RuleConsequence)
    conditions = fields.ListField(fields.EmbeddedDocumentField(RuleCondition))
    active = fields.BooleanField(default=True)
