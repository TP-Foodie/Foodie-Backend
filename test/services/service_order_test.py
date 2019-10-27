from unittest.mock import patch, MagicMock

import pytest
from bson import ObjectId

from models.order import Order
from repositories import order_repository, product_repository
from services import order_service, product_service
from services.exceptions.order_exceptions import NonExistingPlaceException
from services.exceptions.user_exceptions import NonExistingDeliveryException


@pytest.mark.usefixtures('a_client')
class TestOrderService:
    def test_create_order(self, a_customer_user, a_product):
        order_service.create(
            Order.NORMAL_TYPE, a_customer_user.id, {
                'name': a_product.name, 'place': a_product.place.id})

        order = order_repository.list_all()[0]

        assert order.owner.id == a_customer_user.id

    def test_order_number_should_be_consecutive(self, a_customer_user, a_product):
        order_service.create(
            Order.NORMAL_TYPE, a_customer_user.id, {
                'name': a_product.name, 'place': a_product.place.id})
        order_service.create(
            Order.NORMAL_TYPE, a_customer_user.id, {
                'name': a_product.name, 'place': a_product.place.id})

        first_order = order_repository.list_all()[0]
        second_order = order_repository.list_all()[1]

        assert first_order.number == 1
        assert second_order.number == 2

    def test_creating_order_should_create_product_if_it_does_not_exists(
            self, a_customer_user, a_product):
        order_service.create(
            Order.NORMAL_TYPE, a_customer_user.id, {
                'name': "hamburger", 'place': a_product.place.id})

        order = order_repository.list_all()[0]

        assert order.product.id != a_product.id
        assert order.product.name == "hamburger"

    def test_creating_order_should_not_create_product_if_it_exists(self, a_customer_user,
                                                                   a_product):
        order_service.create(
            Order.NORMAL_TYPE, a_customer_user.id, {
                'name': a_product.name, 'place': a_product.place.id})

        order = order_repository.list_all()[0]

        assert order.product.id == a_product.id
        assert product_repository.count() == 1

    def test_create_product_with_invalid_place_id_should_rice_exception(self):
        invalid_place_id = 1

        with pytest.raises(NonExistingPlaceException):
            product_service.create("some_name", invalid_place_id)

    def test_create_product_with_non_existing_place_should_rice_exception(self):
        non_existing_place_id = ObjectId()

        with pytest.raises(NonExistingPlaceException):
            product_service.create("some_name", non_existing_place_id)

    def test_should_create_product_if_its_alright(self, a_place):
        product_service.create("some name", a_place.id)

        assert product_repository.count() == 1

    def test_take_order_updates_status_and_delivery(self, an_order, a_delivery_user):
        order_service.take(an_order.id,
                           {'status': Order.TAKEN_STATUS,
                            'delivery': a_delivery_user.id})

        order = order_repository.get_order(an_order.id)

        assert order.status == Order.TAKEN_STATUS
        assert order.delivery.id == a_delivery_user.id

    def test_take_order_with_non_existing_delivery_raises_error(self, an_order, an_object_id):
        with pytest.raises(NonExistingDeliveryException):
            order_service.take(
                an_order.id, {
                    'status': Order.TAKEN_STATUS, 'delivery': an_object_id})

    def test_count_for_user_return_zero_when_there_are_no_orders_for_user(self, an_order, a_delivery_user):
        assert order_service.count_for_user(a_delivery_user.id) == 0

    def test_count_for_user_returns_user_count(self, an_order):
        assert order_service.count_for_user(an_order.owner.id) == 1

    @patch('services.order_service.requests')
    def test_order_position_returns_order_city(self, mocked_requests, an_order, a_geocode_response, a_city):
        mocked_requests.get.return_value = a_geocode_response

        result = order_service.order_position(an_order)

        assert result == a_city.lower()
