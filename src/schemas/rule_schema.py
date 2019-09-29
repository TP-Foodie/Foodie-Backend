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
