import pytest

from test.support.utils import assert_attr_exists


@pytest.mark.usefixtures('a_client')
class TestRule:
    class TestCondition:
        @pytest.mark.parametrize('attr_name', ['variable', 'operator', 'condition_value'])
        def test_has_attribute(self, attr_name, a_condition):
            assert_attr_exists(a_condition, attr_name)

    class TestConsequence:
        @pytest.mark.parametrize('attr_name', ['consequence_type', 'value'])
        def test_has_attribute(self, attr_name, a_consequence):
            assert_attr_exists(a_consequence, attr_name)

    class TestRule:
        @pytest.mark.parametrize('attr_name', ['conditions', 'consequence', 'name', 'active'])
        def test_has_attribute(self, attr_name, a_rule):
            assert_attr_exists(a_rule, attr_name)
