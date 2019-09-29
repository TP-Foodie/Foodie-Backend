from mongoengine import Document, fields


class RuleCondition(Document):
    variable = fields.StringField(max_length=10)
