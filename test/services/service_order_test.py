import pytest
from bson import ObjectId

from src.models.order import Order
from src.repositories import order_repository, product_repository
from src.services import order_service, product_service
from src.services.exceptions.product_exceptions import NonExistingProductException


@pytest.mark.usefixtures('a_client')
class TestOrderService:
    def test_create_order(self, a_client_user, a_product):
        order_service.create(Order.NORMAL_TYPE, a_client_user.id, {'name': a_product.name, 'place': a_product.place.id})

        order = order_repository.list_all()[0]

        assert order.owner.id == a_client_user.id

    def test_order_number_should_be_consecutive(self, a_client_user, a_product):
        order_service.create(Order.NORMAL_TYPE, a_client_user.id, {'name': a_product.name, 'place': a_product.place.id})
        order_service.create(Order.NORMAL_TYPE, a_client_user.id, {'name': a_product.name, 'place': a_product.place.id})

        first_order = order_repository.list_all()[0]
        second_order = order_repository.list_all()[1]

        assert first_order.number == 1
        assert second_order.number == 2

    def test_creating_order_should_create_product_if_it_does_not_exists(self, a_client_user, a_product):
        order_service.create(Order.NORMAL_TYPE, a_client_user.id, {'name': "hamburger", 'place': a_product.place.id})

        order = order_repository.list_all()[0]

        assert order.product.id != a_product.id
        assert order.product.name == "hamburger"

    def test_creating_order_should_not_create_product_if_it_exists(self, a_client_user, a_product):
        order_service.create(Order.NORMAL_TYPE, a_client_user.id, {'name': a_product.name, 'place': a_product.place.id})

        order = order_repository.list_all()[0]

        assert order.product.id == a_product.id
        assert product_repository.count() == 1

    def test_create_product_with_invalid_place_id_should_rice_exception(self):
        invalid_place_id = 1

        with pytest.raises(NonExistingProductException):
            product_service.create("some_name", invalid_place_id)

    def test_create_product_with_non_existing_place_should_rice_exception(self):
        non_existing_place_id = ObjectId()

        with pytest.raises(NonExistingProductException):
            product_service.create("some_name", non_existing_place_id)
