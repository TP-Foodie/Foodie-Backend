from marshmallow import Schema, fields


class ConditionSchema(Schema):
    class Meta:
        fields = ('variable', 'operator', 'condition_value')


class ConsequenceSchema(Schema):
    class Meta:
        fields = ('consequence_type', 'value', 'variable')


class ListRuleSchema(Schema):
    class Meta:
        fields = ('id', 'name', 'active')


class RuleSchema(Schema):
    conditions = fields.List(fields.Nested(ConditionSchema))
    consequence = fields.Nested(ConsequenceSchema)

    class Meta:
        fields = ('id', 'name', 'active', 'conditions', 'consequence')


class CreateRuleSchema(Schema):
    conditions = fields.List(fields.Nested(ConditionSchema, required=True))
    consequence = fields.Nested(ConsequenceSchema, required=True)
    name = fields.String(required=True)
    active = fields.Boolean(required=False)
    benefit = fields.Boolean(required=False)
