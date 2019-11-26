from unittest.mock import patch

from datetime import datetime
import pytest
from marshmallow import ValidationError
from mongoengine.errors import ValidationError as MongoEngineValidationError

from models.rule import Rule, RuleConsequence, RuleHistory
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

        assert len(Rule.objects.all()) == 2
        assert duplicated.name == a_rule.name
        assert duplicated.conditions == a_rule.conditions
        assert duplicated.consequence == a_rule.consequence
        assert duplicated.active == a_rule.active

    def test_update_rule_adds_previous_version_to_history(self, a_rule):
        self.rule_service.update(a_rule.id, {'name': 'new name'})

        assert RuleHistory.objects.first().versions[0].name == a_rule.name

    def test_rule_history_with_3_versions(self, a_rule):
        self.rule_service.update(a_rule.id, {'name': 'new name'})
        self.rule_service.update(a_rule.id, {'name': 'new name2'})

        history = RuleHistory.objects.first()

        assert len(history.versions) == 2
        assert history.versions[0].name == a_rule.name
        assert history.versions[1].name == 'new name'

    def test_adding_to_rule_history_does_not_modify_actual_rule(self, a_rule):
        self.rule_service.update(a_rule.id, {'name': 'new name'})

        updated = Rule.objects.get(id=a_rule.id)

        assert updated.id == a_rule.id

    def test_history_returns_rule_history(self, a_rule):
        self.rule_service.update(a_rule.id, {'name': 'new name'})

        history = self.rule_service.history(a_rule.id)

        assert history.versions[0].name == a_rule.name

    def test_history_when_rule_was_never_updated_returns_rule(self, a_rule):
        history = self.rule_service.history(a_rule.id)

        assert not history.versions
        assert history.rule == a_rule

# noinspection PyTypeChecker
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
        an_order.date = datetime.strptime('Sat, 30 Nov 2019 18:30:00 -0300',
                                          "%a, %d %b %Y %H:%M:%S %z")
        an_order.save()

        Rule(
            name='5% discount today',
            conditions=[
                RuleCondition(
                    variable=RuleCondition.ORDER_DATE,
                    operator=RuleCondition.IS,
                    condition_value='Sat, 30 Nov 2019 18:30:00 -0300'
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

    @patch('services.order_service.requests.get')
    def test_quote_price_with_distance_rule(self, mocked_get, an_order, a_distance_response):
        mocked_get.return_value = a_distance_response(54)

        # to Escobar
        an_order.owner.location.latitude = -34.3467
        an_order.owner.location.longitude = -58.8186
        an_order.owner.save()

        # from Buenos Aires
        an_order.ordered_products[0].product.place.coordinates.latitude = -34.603722
        an_order.ordered_products[0].product.place.coordinates.longitude = -58.381592
        an_order.ordered_products[0].product.place.save()

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

    @patch('services.order_service.requests.get')
    def test_quote_price_with_location_rule(self, mocked_get, an_order, a_geocode_response):
        mocked_get.return_value = a_geocode_response('Ingeniero Maschwitz')
        # Ing Maschwitz
        an_order.owner.location.latitude = -34.3814
        an_order.owner.location.longitude = -58.7569
        an_order.owner.save()

        Rule(
            name='$200 if order is in Ingeniero Maschwitz',
            conditions=[
                RuleCondition(
                    variable=RuleCondition.ORDER_POSITION,
                    operator=RuleCondition.IS,
                    condition_value='Ingeniero Maschwitz'
                ),
            ],
            consequence=RuleConsequence(consequence_type=RuleConsequence.VALUE, value=200)
        ).save()

        assert self.rule_service.quote_price(an_order.id) == 200

    @patch('services.order_service.requests.get')
    def test_quote_price_with_location_rule_should_work_lower_case(self, mocked_get,
                                                                   an_order, a_geocode_response):
        mocked_get.return_value = a_geocode_response('Ingeniero Maschwitz')

        # Ing Maschwitz
        an_order.owner.location.latitude = -34.3814
        an_order.owner.location.longitude = -58.7569
        an_order.owner.save()

        Rule(
            name='$200 if order is in ingeniero maschwitz',
            conditions=[
                RuleCondition(
                    variable=RuleCondition.ORDER_POSITION,
                    operator=RuleCondition.IS,
                    condition_value='ingeniero maschwitz'
                ),
            ],
            consequence=RuleConsequence(consequence_type=RuleConsequence.VALUE, value=200)
        ).save()

        assert self.rule_service.quote_price(an_order.id) == 200

    @patch('services.order_service.requests.get')
    def test_quote_price_with_value_per_unit_consequence(self, mocked_get,
                                                         an_order, a_distance_response):
        mocked_get.return_value = a_distance_response(54)

        # to Escobar
        an_order.owner.location.latitude = -34.3467
        an_order.owner.location.longitude = -58.8186
        an_order.owner.save()

        # from Buenos Aires
        an_order.ordered_products[0].product.place.coordinates.latitude = -34.603722
        an_order.ordered_products[0].product.place.coordinates.longitude = -58.381592
        an_order.ordered_products[0].product.place.save()

        Rule(
            name='$20 per km',
            conditions=[
                RuleCondition(
                    variable=RuleCondition.ORDER_DISTANCE,
                    operator=RuleCondition.GREATER_THAN_EQUAL,
                    condition_value='20'
                ),
            ],
            consequence=RuleConsequence(
                consequence_type=RuleConsequence.PER_UNIT_VALUE,
                value=20,
                variable=RuleCondition.ORDER_DISTANCE
            )
        ).save()

        assert self.rule_service.quote_price(an_order.id) == 20 * 54

    def test_should_not_apply_rule_if_its_not_active(self, an_order):
        rule = Rule(
            name='$20 base',
            conditions=[
                RuleCondition(
                    variable=RuleCondition.USER_REPUTATION,
                    operator=RuleCondition.GREATER_THAN_EQUAL,
                    condition_value='0'
                ),
            ],
            consequence=RuleConsequence(
                consequence_type=RuleConsequence.VALUE,
                value=20,
            )
        ).save()

        rule.active = False
        rule.save()

        assert self.rule_service.quote_price(an_order.id) == 0

    def test_should_return_zero_if_quotation_is_negative(self, an_order):
        Rule(
            name='$20 discount',
            conditions=[
                RuleCondition(
                    variable=RuleCondition.USER_REPUTATION,
                    operator=RuleCondition.GREATER_THAN_EQUAL,
                    condition_value='0'
                ),
            ],
            consequence=RuleConsequence(
                consequence_type=RuleConsequence.VALUE,
                value=-20,
            )
        ).save()

        assert self.rule_service.quote_price(an_order.id) == 0


# noinspection PyTypeChecker
@pytest.mark.usefixtures('a_client')
class TestExampleRules:
    rule_service = RuleService()

    def assert_price(self, order, expected):
        assert self.rule_service.quote_price(order.id) == expected

    @patch('services.order_service.requests.get')
    def test_minimum_delivery_cost(self, mocked_get, an_order, a_distance_response):
        mocked_get.return_value = a_distance_response(1)

        Rule(
            name='Minimum delivery cost of $20',
            conditions=[
                RuleCondition(
                    variable=RuleCondition.ORDER_DISTANCE,
                    operator=RuleCondition.GREATER_THAN_EQUAL,
                    condition_value='0'
                ),
            ],
            consequence=RuleConsequence(consequence_type=RuleConsequence.VALUE, value=20)
        ).save()

        self.assert_price(an_order, 20)

    @patch('services.order_service.requests.get')
    def test_price_per_extra_km(self, mocked_get, an_order, a_distance_response):
        mocked_get.return_value = a_distance_response(54)

        # to Escobar
        an_order.owner.location.latitude = -34.3467
        an_order.owner.location.longitude = -58.8186
        an_order.owner.save()

        # from Buenos Aires
        an_order.ordered_products[0].product.place.coordinates.latitude = -34.603722
        an_order.ordered_products[0].product.place.coordinates.longitude = -58.381592
        an_order.ordered_products[0].product.place.save()

        Rule(
            name='$15 per extra kilometer above 2',
            conditions=[
                RuleCondition(
                    variable=RuleCondition.ORDER_DISTANCE,
                    operator=RuleCondition.GREATER_THAN,
                    condition_value='2'
                ),
            ],
            consequence=RuleConsequence(
                consequence_type=RuleConsequence.PER_UNIT_VALUE,
                value=15,
                variable=RuleCondition.ORDER_DISTANCE
            )
        ).save()

        Rule(
            name='discount first 2km',
            conditions=[
                RuleCondition(
                    variable=RuleCondition.ORDER_DISTANCE,
                    operator=RuleCondition.GREATER_THAN_EQUAL,
                    condition_value='2'
                ),
            ],
            consequence=RuleConsequence(
                consequence_type=RuleConsequence.VALUE,
                value=-30,
            )
        ).save()

        self.assert_price(an_order, 52 * 15)

    def test_five_percent_discount_wednesdays_from_three_pm_to_four_pm(self, an_order_factory):
        an_order = an_order_factory()
        an_order.date = datetime.strptime('Wed, 27 Nov 2019 15:30:00 GMT',
                                          "%a, %d %b %Y %H:%M:%S %Z")
        an_order.save()

        another_order = an_order_factory()
        another_order .date = datetime.strptime('Wed, 27 Nov 2019 16:30:00 GMT',
                                                "%a, %d %b %Y %H:%M:%S %Z")
        another_order.save()

        Rule(
            name='Minimum delivery cost of $20',
            conditions=[
                RuleCondition(
                    variable=RuleCondition.USER_REPUTATION,
                    operator=RuleCondition.GREATER_THAN_EQUAL,
                    condition_value='0'
                ),
            ],
            consequence=RuleConsequence(consequence_type=RuleConsequence.VALUE, value=20)
        ).save()

        Rule(
            name='5% discount on wednesdays from 3pm to 4pm',
            conditions=[
                RuleCondition(
                    variable=RuleCondition.ORDER_DAY,
                    operator=RuleCondition.IS,
                    condition_value='3'
                ),
                RuleCondition(
                    variable=RuleCondition.ORDER_TIME,
                    operator=RuleCondition.GREATER_THAN_EQUAL,
                    condition_value='Sat, 30 Nov 2019 15:00:00 -0300'
                ),
                RuleCondition(
                    variable=RuleCondition.ORDER_TIME,
                    operator=RuleCondition.LESS_THAN_EQUAL,
                    condition_value='Sat, 30 Nov 2019 16:00:00 -0300'
                )
            ],
            consequence=RuleConsequence(
                consequence_type=RuleConsequence.PERCENTAGE,
                value=-5,
            )
        ).save()

        self.assert_price(an_order, 19.0)
        self.assert_price(another_order, 20)

    def test_100_discount_on_first_order(self, an_order_factory):
        an_order = an_order_factory()

        Rule(
            name='$100 discount on first order',
            conditions=[
                RuleCondition(
                    variable=RuleCondition.ORDER_QUANTITY,
                    operator=RuleCondition.IS,
                    condition_value='1'
                ),
            ],
            consequence=RuleConsequence(consequence_type=RuleConsequence.VALUE, value=-100)
        ).save()

        self.assert_price(an_order, 0)

        an_order_factory()

        self.assert_price(an_order, 0)

    def test_recharge_of_10_from_monday_to_friday_from_5_pm_to_7_pm(self, an_order_factory):
        an_order = an_order_factory()
        an_order.date = datetime.strptime('Wed, 27 Nov 2019 17:30:00 GMT',
                                          "%a, %d %b %Y %H:%M:%S %Z")
        an_order.save()

        another_order = an_order_factory()
        another_order.date = datetime.strptime('Sat, 30 Nov 2019 17:30:00 GMT',
                                               "%a, %d %b %Y %H:%M:%S %Z")
        another_order.save()

        Rule(
            name='$10 recharge from monday to friday from 5pm to 7pm',
            conditions=[
                RuleCondition(
                    variable=RuleCondition.ORDER_DAY,
                    operator=RuleCondition.GREATER_THAN_EQUAL,
                    condition_value='1'
                ),
                RuleCondition(
                    variable=RuleCondition.ORDER_DAY,
                    operator=RuleCondition.LESS_THAN_EQUAL,
                    condition_value='5'
                ),
                RuleCondition(
                    variable=RuleCondition.ORDER_TIME,
                    operator=RuleCondition.GREATER_THAN_EQUAL,
                    condition_value='Sat, 30 Nov 2019 15:00:00 -0300'
                ),
                RuleCondition(
                    variable=RuleCondition.ORDER_TIME,
                    operator=RuleCondition.LESS_THAN_EQUAL,
                    condition_value='Sat, 30 Nov 2019 19:00:00 -0300'
                ),
            ],
            consequence=RuleConsequence(consequence_type=RuleConsequence.VALUE, value=10)
        ).save()

        self.assert_price(an_order, 10)
        self.assert_price(another_order, 0)

    def test_20_percent_discount_from_fifth_order(self, an_order_factory):
        an_order = an_order_factory()
        an_order_factory()
        an_order_factory()
        an_order_factory()
        an_order_factory()

        Rule(
            name='Minimum delivery cost of $20',
            conditions=[
                RuleCondition(
                    variable=RuleCondition.USER_REPUTATION,
                    operator=RuleCondition.GREATER_THAN_EQUAL,
                    condition_value='0'
                ),
            ],
            consequence=RuleConsequence(consequence_type=RuleConsequence.VALUE, value=20)
        ).save()

        Rule(
            name='%20 discount from 5th order',
            conditions=[
                RuleCondition(
                    variable=RuleCondition.ORDER_QUANTITY,
                    operator=RuleCondition.GREATER_THAN_EQUAL,
                    condition_value='5'
                ),
            ],
            consequence=RuleConsequence(consequence_type=RuleConsequence.PERCENTAGE, value=-20)
        ).save()

        self.assert_price(an_order, 16)


# noinspection PyTypeChecker
@pytest.mark.usefixtures('a_client')
class TestBenefitsRules:
    rule_service = RuleService()

    def test_benefit_rules_do_not_apply_to_flat_users(self, a_customer_user, an_order):
        an_order.owner = a_customer_user
        an_order.save()

        Rule(
            name='Minimum delivery cost of $10 for premium users',
            conditions=[
                RuleCondition(
                    variable=RuleCondition.USER_REPUTATION,
                    operator=RuleCondition.GREATER_THAN_EQUAL,
                    condition_value='0'
                ),
            ],
            consequence=RuleConsequence(consequence_type=RuleConsequence.VALUE, value=10),
            benefit=True
        ).save()

        assert not self.rule_service.quote_price(an_order.id)

    def test_benefits_returns_all_benefits_rules(self, a_benefit_rule):
        assert len(self.rule_service.benefits()) == 1
        assert self.rule_service.benefits()[0]['id'] == a_benefit_rule.id

    def test_list_rules_should_not_include_benefits(self, another_rule, a_benefit_rule):
        # pylint: disable=unused-argument
        assert len(self.rule_service.list()) == 1
        assert self.rule_service.list()[0]['id'] == another_rule.id
