import pytest
from marshmallow import ValidationError
from mongoengine.errors import ValidationError as MongoEngineValidationError

from models.rule import Rule, RuleConsequence
from services.rule_service import RuleService


@pytest.mark.usefixtures('a_client')
class TestRuleService:
    rule_service = RuleService()

    def test_create_rule_with_no_consequence_should_raise_error(self, a_condition):
        with pytest.raises(ValidationError):
            self.rule_service.create(condition=a_condition, name='a rule')

    def test_create_rule_with_consequence(self, a_condition_data, a_consequence_data):
        self.rule_service.create(
            conditions=[a_condition_data],
            consequence=a_consequence_data,
            name='a rule'
        )

        assert Rule.objects.count() == 1

    def test_create_rule_with_name(self, a_condition_data, a_consequence_data):
        rule = self.rule_service.create(
            conditions=[a_condition_data],
            consequence=a_consequence_data,
            name='a rule'
        )

        assert rule.name == 'a rule'

    def test_update_rule_should_update_its_fields(self, a_rule):
        self.rule_service.update(a_rule.id, {'name': 'new name'})

        assert Rule.objects.get(id=a_rule.id).name == 'new name'

    def test_update_does_not_duplicate(self, a_rule):
        self.rule_service.update(a_rule.id, {'name': 'new name'})

        assert Rule.objects.count() == 1

    def test_update_with_invalid_field_throws_error(self, a_rule):
        with pytest.raises(MongoEngineValidationError):
            self.rule_service.update(a_rule.id, {'conditions': [{'variable': 'DOES NOT EXISTS'}]})

    def test_delete_rule_removes_it(self, a_rule):
        self.rule_service.delete(a_rule.id)
        assert not Rule.objects.count()


@pytest.mark.usefixtures('a_client')
class TestPriceQuote:
    rule_service = RuleService()

    def test_should_return_zero_if_no_conditions(self, a_consequence, an_order):
        Rule(
            name='new rule',
            conditions=[],
            consequence=a_consequence
        ).save()
        assert self.rule_service.quote_price(an_order.id) == 0

    def test_should_apply_consequence_if_no_condition(self, an_order):
        Rule(
            name='new rule',
            conditions=[],
            consequence=RuleConsequence(consequence_type=RuleConsequence.VALUE, value=5)
        ).save()
        assert self.rule_service.quote_price(an_order.id) == 5
