import pytest

from test.support.utils import assert_attr_exists


@pytest.mark.usefixtures('a_client')
class TestCondition:
    @pytest.mark.parametrize('attr_name', ['variable'])
    def test_has_attribute(self, attr_name, a_condition):
        assert_attr_exists(a_condition, attr_name)

