import pytest
from datetime import datetime
from marshmallow import ValidationError
from mongoengine.errors import ValidationError as MongoEngineValidationError

from models.rule import Rule, RuleConsequence
from models.rule import RuleCondition
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

    def test_apply_consequence_with_one_rule(self, an_order):
        Rule(
            name='new rule',
            conditions=[
                RuleCondition(
                    variable=RuleCondition.USER_REPUTATION,
                    operator=RuleCondition.LESS_THAN,
                    condition_value='2'
                )
            ],
            consequence=RuleConsequence(consequence_type=RuleConsequence.VALUE, value=5)
        ).save()

        an_order.owner.reputation = 1
        an_order.owner.save()

        assert self.rule_service.quote_price(an_order.id) == 5

    def test_percentage_consequence_should_apply_over_total(self, an_order):
        Rule(
            name='new rule',
            conditions=[
                RuleCondition(
                    variable=RuleCondition.USER_REPUTATION,
                    operator=RuleCondition.LESS_THAN,
                    condition_value='2'
                ),
            ],
            consequence=RuleConsequence(consequence_type=RuleConsequence.VALUE, value=10)
        ).save()

        Rule(
            name='new rule',
            conditions=[
                RuleCondition(
                    variable=RuleCondition.USER_REPUTATION,
                    operator=RuleCondition.LESS_THAN,
                    condition_value='2'
                ),
            ],
            consequence=RuleConsequence(consequence_type=RuleConsequence.PERCENTAGE, value=-10)
        ).save()

        assert self.rule_service.quote_price(an_order.id) == 9

    def test_percentage_consequence_should_apply_last(self, an_order):
        Rule(
            name='new rule',
            conditions=[
                RuleCondition(
                    variable=RuleCondition.USER_REPUTATION,
                    operator=RuleCondition.LESS_THAN,
                    condition_value='2'
                ),
            ],
            consequence=RuleConsequence(consequence_type=RuleConsequence.PERCENTAGE, value=-10)
        ).save()

        Rule(
            name='new rule',
            conditions=[
                RuleCondition(
                    variable=RuleCondition.USER_REPUTATION,
                    operator=RuleCondition.LESS_THAN,
                    condition_value='2'
                ),
            ],
            consequence=RuleConsequence(consequence_type=RuleConsequence.VALUE, value=10)
        ).save()

        assert self.rule_service.quote_price(an_order.id) == 9

    def test_quote_price_with_datetime_rules(self, an_order):
        an_order.date = datetime.strptime('Sat, 30 Nov 2019 18:30:00 GMT', "%a, %d %b %Y %H:%M:%S %Z")
        an_order.save()

        Rule(
            name='5% discount today',
            conditions=[
                RuleCondition(
                    variable=RuleCondition.ORDER_DATE,
                    operator=RuleCondition.IS,
                    condition_value='Sat, 30 Nov 2019 18:30:00 GMT'
                ),
            ],
            consequence=RuleConsequence(consequence_type=RuleConsequence.PERCENTAGE, value=-5)
        ).save()
        Rule(
            name='base price',
            conditions=[
                RuleCondition(
                    variable=RuleCondition.USER_REPUTATION,
                    operator=RuleCondition.GREATER_THAN_EQUAL,
                    condition_value='0'
                ),
            ],
            consequence=RuleConsequence(consequence_type=RuleConsequence.VALUE, value=20)
        ).save()

        assert self.rule_service.quote_price(an_order.id) == 19

    def test_quote_price_with_distance_rule(self, an_order):
        # to Escobar
        an_order.owner.location.latitude = -34.3467
        an_order.owner.location.longitude = -58.8186
        an_order.owner.save()

        # from Buenos Aires
        an_order.product.place.coordinates.latitude = -34.603722
        an_order.product.place.coordinates.longitude = -58.381592
        an_order.product.place.save()

        Rule(
            name='$200 if distance is greater than 50km',
            conditions=[
                RuleCondition(
                    variable=RuleCondition.ORDER_DISTANCE,
                    operator=RuleCondition.GREATER_THAN,
                    condition_value='50'
                ),
            ],
            consequence=RuleConsequence(consequence_type=RuleConsequence.VALUE, value=200)
        ).save()

        # rule should apply cause the distance is ~54 > 50
        assert self.rule_service.quote_price(an_order.id) == 200

    def test_quote_price_with_location_rule(self, an_order):
        # Ing Maschwitz
        an_order.owner.location.latitude = -34.3814
        an_order.owner.location.longitude = -58.7569
        an_order.owner.save()

        Rule(
            name='$200 if order is in Escobar',
            conditions=[
                RuleCondition(
                    variable=RuleCondition.ORDER_POSITION,
                    operator=RuleCondition.IS,
                    condition_value='Ingeniero Maschwitz'
                ),
            ],
            consequence=RuleConsequence(consequence_type=RuleConsequence.VALUE, value=200)
        ).save()

        # rule should apply cause Maschwitz is in Escobar
        assert self.rule_service.quote_price(an_order.id) == 200

    def test_quote_price_with_location_rule_should_work_lower_case(self, an_order):
        # Ing Maschwitz
        an_order.owner.location.latitude = -34.3814
        an_order.owner.location.longitude = -58.7569
        an_order.owner.save()

        Rule(
            name='$200 if order is in Escobar',
            conditions=[
                RuleCondition(
                    variable=RuleCondition.ORDER_POSITION,
                    operator=RuleCondition.IS,
                    condition_value='ingeniero maschwitz'
                ),
            ],
            consequence=RuleConsequence(consequence_type=RuleConsequence.VALUE, value=200)
        ).save()

        # rule should apply cause Maschwitz is in Escobar
        assert self.rule_service.quote_price(an_order.id) == 200


