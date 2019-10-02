from marshmallow import Schema, fields


class ConditionSchema(Schema):
    class Meta:
        fields = ('variable', 'operator', 'condition_value')


class ConsequenceSchema(Schema):
    class Meta:
        fields = ('consequence_type', 'value')


class ListRuleSchema(Schema):
    class Meta:
        fields = ('id', 'name', 'active')


class RuleSchema(Schema):
    condition = fields.Nested(ConditionSchema)
    consequence = fields.Nested(ConsequenceSchema)

    class Meta:
        fields = ('id', 'name', 'active', 'condition', 'consequence')


class CreateRuleSchema(Schema):
    condition = fields.Nested(ConditionSchema, required=True)
    consequence = fields.Nested(ConsequenceSchema, required=True)
    name = fields.String(required=True)
