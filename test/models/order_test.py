import pytest

from test.support.utils import assert_attr_exists


class TestOrder:
    @pytest.mark.parametrize('attr_name', ['number', 'status', 'type', 'owner'])
    def test_should_answer_to_attr(self, attr_name, an_order):
        assert_attr_exists(an_order, attr_name)
