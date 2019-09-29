from marshmallow import Schema, fields


class ConditionSchema(Schema):
    class Meta:
        fields = ('variable', 'operator', 'condition_value')


class ConsequenceSchema(Schema):
    class Meta:
        fields = ('consequence_type', 'value')


class RuleSchema(Schema):
    condition = fields.Nested(ConditionSchema)
    consequence = fields.Nested(ConsequenceSchema)

    class Meta:
        fields = ('id', 'name', 'condition', 'consequence')
