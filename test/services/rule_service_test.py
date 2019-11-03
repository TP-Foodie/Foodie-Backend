import pytest
from marshmallow import ValidationError
from mongoengine.errors import ValidationError as MongoEngineValidationError

from models.rule import Rule, RuleHistory
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

    def test_update_rule_should_create_history(self, a_rule):
        self.rule_service.update(a_rule.id, {'name': 'new name'})

        assert RuleHistory.objects.count() == 1

    def test_duplicate_rule_duplicates_all_fields_but_id(self, a_rule):
        duplicated = self.rule_service.duplicate(a_rule.id)

        assert len(self.rule_service.list()) == 2
        assert duplicated.name == a_rule.name
        assert duplicated.conditions == a_rule.conditions
        assert duplicated.consequence == a_rule.consequence
        assert duplicated.active == a_rule.active

    def test_update_rule_adds_previous_version_to_history(self, a_rule):
        self.rule_service.update(a_rule.id, {'name': 'new name'})

        assert RuleHistory.objects.first().versions == a_rule

