from marshmallow import Schema, fields, validates_schema, ValidationError


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
        fields = ('id', 'name', 'active', 'conditions', 'consequence', 'redeemable')


class CreateRuleSchema(Schema):
    conditions = fields.List(fields.Nested(ConditionSchema, required=True))
    consequence = fields.Nested(ConsequenceSchema, required=True)
    name = fields.String(required=True)
    active = fields.Boolean(required=False)
    benefit = fields.Boolean(required=False)
    redeemable = fields.Boolean(required=False)
    cost = fields.Int(required=False)

    @validates_schema
    def validate_schema(self, data, **kwargs):
        if data.get('redeemable') and not data.get('benefit'):
            raise ValidationError('redeemable rules must be benefits')


class RuleVersionSchema(Schema):
    conditions = fields.List(fields.Nested(ConditionSchema))
    consequence = fields.Nested(ConsequenceSchema)

    class Meta:
        fields = ('name', 'active', 'conditions', 'consequence')


class RuleHistorySchema(Schema):
    rule = fields.Nested(RuleSchema)
    versions = fields.List(fields.Nested(RuleVersionSchema))
