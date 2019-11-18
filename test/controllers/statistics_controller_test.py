from test.support.utils import TestMixin, assert_401


class TestStatisticsController(TestMixin):
    def test_registrations_for_unauthenticated(self, a_client):
        response = a_client.get('api/v1/statistics/registrations')

        assert_401(response)
