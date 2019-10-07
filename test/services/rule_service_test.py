import pytest
from marshmallow import ValidationError
from mongoengine.errors import ValidationError as MongoEngineValidationError

from src.models.rule import Rule
from src.services.rule_service import RuleService


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
