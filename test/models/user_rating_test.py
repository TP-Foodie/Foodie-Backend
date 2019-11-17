import pytest

from test.support.utils import assert_attr_exists


@pytest.mark.usefixtures('a_client')
class TestUserRating:
    @pytest.mark.parametrize('attr_name', ['user', 'description', 'rating'])
    def test_has_attribute(self, attr_name, a_user_rating):
        assert_attr_exists(a_user_rating, attr_name)
