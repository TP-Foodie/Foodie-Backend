from datetime import datetime, timedelta
from unittest.mock import patch

import pytest

from models import User
from models.order import Order
from models.rule import RuleCondition, RuleConsequence, Rule
from repositories import order_repository, user_repository
from services import order_service
from services.exceptions.order_exceptions import NotEnoughGratitudePointsException
from services.exceptions.user_exceptions import NonExistingDeliveryException


@pytest.mark.usefixtures('a_client')
class TestOrderService: # pylint: disable=too-many-public-methods
    def test_create_order(self, a_customer_user, an_ordered_product):
        order_service.create(
            "name",
            Order.NORMAL_TYPE,
            [{'quantity': an_ordered_product.quantity, 'product': an_ordered_product.product.id}],
            'CPM', a_customer_user.id
        )

        order = order_repository.list_all()[0]

        assert order.owner.id == a_customer_user.id
        assert order.name == "name"

    def test_order_number_should_be_consecutive(self, a_customer_user, an_ordered_product):
        order_service.create(
            "name",
            Order.NORMAL_TYPE,
            [{'quantity': an_ordered_product.quantity, 'product': an_ordered_product.product.id}],
            'CPM', a_customer_user.id
        )
        order_service.create(
            "name2",
            Order.NORMAL_TYPE,
            [{'quantity': an_ordered_product.quantity, 'product': an_ordered_product.product.id}],
            'CPM', a_customer_user.id
        )

        first_order = order_repository.list_all()[0]
        second_order = order_repository.list_all()[1]

        assert first_order.number == 1
        assert second_order.number == 2

    def test_take_order_updates_status_and_delivery(self, an_order, a_delivery_user):
        order_service.take(an_order.id, a_delivery_user.id)

        order = order_repository.get_order(an_order.id)
        delivery = user_repository.get_user(a_delivery_user.id)

        assert order.status == Order.TAKEN_STATUS
        assert order.delivery.id == a_delivery_user.id
        assert not delivery.available

    def test_deliver_order_updates_status_and_delivery(self, an_order, a_delivery_user):
        order_service.deliver(an_order.id)

        order = order_repository.get_order(an_order.id)
        delivery = user_repository.get_user(a_delivery_user.id)

        assert order.status == Order.DELIVERED_STATUS
        assert order.delivery.id == a_delivery_user.id
        assert delivery.available

    def test_cancel_order_updates_status_and_delivery(self, an_order, a_delivery_user):
        order_service.take(an_order.id, a_delivery_user.id)

        delivery = user_repository.get_user(a_delivery_user.id)
        assert not delivery.available
        assert delivery is not None

        order_service.update(an_order.id, {'status': Order.CANCELLED_STATUS})
        order = order_repository.get_order(an_order.id)
        delivery = user_repository.get_user(a_delivery_user.id)

        assert order.status == Order.CANCELLED_STATUS
        assert order.delivery is None
        assert order.quotation == 0
        assert delivery.available

    def test_unassign_order_updates_status_and_delivery(self, an_order, a_delivery_user):
        order_service.take(an_order.id, a_delivery_user.id)

        delivery = user_repository.get_user(a_delivery_user.id)
        assert not delivery.available

        order_service.update(an_order.id, {'status': Order.WAITING_STATUS})
        order = order_repository.get_order(an_order.id)
        delivery = user_repository.get_user(a_delivery_user.id)

        assert order.status == Order.WAITING_STATUS
        assert order.delivery is None
        assert order.quotation == 0
        assert delivery.available

    def test_take_order_with_non_existing_delivery_raises_error(self, an_order, an_object_id):
        with pytest.raises(NonExistingDeliveryException):
            order_service.take(an_order.id, an_object_id)

    def test_placed_by_returns_orders_placed_by_user(self, an_order, a_customer_user):
        an_order.owner = a_customer_user
        an_order.save()

        orders = order_service.placed_by(a_customer_user.id)

        assert orders[0] == an_order

    def test_placed_by_returns_users_only(self, an_order_factory, a_customer_user, a_delivery_user):
        an_order = an_order_factory()
        an_order.owner = a_customer_user
        an_order.save()

        another_order = an_order_factory()
        another_order.owner = a_delivery_user
        another_order.save()

        orders = order_service.placed_by(a_customer_user.id)

        assert len(orders) == 1
        assert orders[0] == an_order

    def test_placed_by_with_dates_return_placed_orders_between_dates(self, an_order,
                                                                     a_customer_user):
        today = datetime.today()
        yesterday = today - timedelta(days=1)
        tomorrow = today + timedelta(days=1)

        an_order.owner = a_customer_user
        an_order.created = tomorrow
        an_order.save()

        orders = order_service.placed_by(a_customer_user.id, yesterday, today)

        assert not orders

    def test_count_for_user_return_zero_when_there_are_no_orders_for_user(self,
                                                                          an_order,
                                                                          a_delivery_user):
        # pylint: disable=unused-argument
        assert order_service.count_for_user(a_delivery_user.id) == 0

    def test_count_for_user_returns_user_count(self, an_order):
        assert order_service.count_for_user(an_order.owner.id) == 1

    @patch('services.order_service.requests')
    def test_order_position_returns_order_city(self, mocked_requests, an_order,
                                               a_geocode_response, a_city):
        mocked_requests.get.return_value = a_geocode_response(a_city)

        result = order_service.order_position(an_order)

        assert result == a_city.lower()

    def test_order_directions_for_order_without_delivery_returns_empty(self, an_order):
        an_order.delivery = None
        an_order.save()

        assert not order_service.directions(an_order.id)

    @patch('services.order_service.requests.get')
    def test_order_directions_requests_directions(self, mocked_get,
                                                  an_order, a_directions_response):
        mocked_get.return_value = a_directions_response
        order_service.directions(an_order.id)

        assert mocked_get.called

    def test_deliver_order_should_increase_delivery_balance_by_85_percent_of_cost(self, an_order):
        an_order.quotation = 100
        an_order.save()

        order_service.deliver(an_order.id)

        assert an_order.delivery.balance == 85

    # noinspection PyTypeChecker
    def test_should_calculate_quotation_based_on_rules(self, an_order, a_delivery_user):
        Rule(
            name='$20 base',
            conditions=[],
            consequence={'consequence_type': RuleConsequence.VALUE, 'value': 20}
        ).save()

        order_service.take(an_order.id, a_delivery_user.id)

        assert Order.objects.get(id=an_order.id).quotation == 20

    def test_create_favor_order_if_user_has_not_enough_gratitude_points_raises_error(self, a_customer_user, a_product):  # pylint: disable=line-too-long
        a_customer_user.gratitude_points = 0
        a_customer_user.save()

        with pytest.raises(NotEnoughGratitudePointsException):
            order_service.create(
                'some order',
                Order.FAVOR_TYPE,
                [{'quantity': 1, 'product': a_product.id}],
                RuleCondition.GRATITUDE_POINTS_PAYMENT_METHOD,
                a_customer_user.id,
                5,
            )

    def test_create_favor_order_with_no_gratitude_points_should_create_one_with_zero(self, a_customer_user, a_product):  # pylint: disable=line-too-long
        order = order_service.create(
            'some order',
            Order.FAVOR_TYPE,
            [{'quantity': 1, 'product': a_product.id}],
            RuleCondition.GRATITUDE_POINTS_PAYMENT_METHOD,
            a_customer_user.id
        )

        assert order.gratitude_points == 0

    def test_create_favor_order_with_gratitude_points_should_create_it(self,
                                                                       a_customer_user,
                                                                       a_product):
        a_customer_user.gratitude_points = 10
        a_customer_user.save()

        order = order_service.create(
            'some order',
            Order.FAVOR_TYPE,
            [{'quantity': 1, 'product': a_product.id}],
            RuleCondition.GRATITUDE_POINTS_PAYMENT_METHOD,
            a_customer_user.id,
            5
        )

        assert order.gratitude_points == 5

    def test_deliver_favor_order_should_add_gratitude_points_to_delivery(self, a_favor_order,
                                                                         a_customer_user,
                                                                         another_customer_user):
        a_favor_order.gratitude_points = 5
        a_favor_order.save()

        a_customer_user.gratitude_points = 10
        a_customer_user.save()

        order_service.take(a_favor_order.id, another_customer_user.id)
        order_service.deliver(a_favor_order.id)

        assert User.objects.get(id=another_customer_user.id).gratitude_points == 15
        assert User.objects.get(id=a_customer_user.id).gratitude_points == 5

    # noinspection PyTypeChecker
    def test_take_favor_order_should_not_calculate_quotation(self,
                                                             a_favor_order,
                                                             another_customer_user):
        Rule(
            name='$20 base',
            conditions=[],
            consequence={'consequence_type': RuleConsequence.VALUE, 'value': 20}
        ).save()

        order_service.take(a_favor_order.id, another_customer_user.id)

        assert Order.objects.get(id=a_favor_order.id).quotation == 0

    def test_completed_by_date_returns_empty_list_if_no_orders_are_completed(self, an_order):
        # pylint: disable=unused-argument
        assert not order_service.completed_by_date()

    def test_completed_by_date_returns_orders_completed_by_date(self, a_complete_order):
        orders = order_service.completed_by_date()

        assert len(orders) == 1
        assert orders[0]['count'] == 1
        assert orders[0]['date'].date() == a_complete_order.completed_date.date()

    def test_deliver_order_should_set_completed_date_field(self, an_order):
        order_service.deliver(an_order.id)

        assert Order.objects.get(id=an_order.id).completed_date.date() == datetime.today().date()

    def test_cancelled_by_date_returns_empty_list_if_no_orders_are_cancelled(self, an_order):
        # pylint: disable=unused-argument
        assert not order_service.cancelled_by_date()

    def test_cancelled_by_date_returns_orders_cancelled_by_date(self, a_cancelled_order):
        orders = order_service.cancelled_by_date()

        assert len(orders) == 1
        assert orders[0]['count'] == 1
        assert orders[0]['date'].date() == a_cancelled_order.completed_date.date()
