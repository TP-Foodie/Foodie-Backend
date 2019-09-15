import pytest

from src.models.order import OrderWaitingStatus, OrderNormalType
from test.support.utils import assert_attr_exists


class TestOrder:
    @pytest.mark.parametrize('attr_name', ['number', 'status', 'type', 'owner'])
    def test_should_answer_to_attr(self, attr_name, an_order):
        assert_attr_exists(an_order, attr_name)

    def test_order_should_be_on_waiting_status_by_default(self, an_order):
        assert isinstance(an_order.status, OrderWaitingStatus)

    def test_order_should_be_of_normal_type_by_default(self, an_order):
        assert isinstance(an_order.type, OrderNormalType)