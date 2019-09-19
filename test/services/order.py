import pytest

from src.models.order import Order
from src.repositories import order_repository
from src.services import order_service


@pytest.mark.usefixtures('a_client')
class TestOrderService:
    def test_create_order(self, a_client_user, a_product):
        order_service.create(Order.NORMAL_TYPE, a_client_user.id, a_product.id)

        order = order_repository.list_all()[0]

        assert order.owner.id == a_client_user.id
        assert order.product.id == a_product.id

    def test_order_number_should_be_consecutive(self, a_client_user, a_product):
        order_service.create(Order.NORMAL_TYPE, a_client_user.id, a_product.id)
        order_service.create(Order.NORMAL_TYPE, a_client_user.id, a_product.id)

        first_order = order_repository.list_all()[0]
        second_order = order_repository.list_all()[1]

        assert first_order.number == 1
        assert second_order.number == 2
