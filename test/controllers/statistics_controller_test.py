import json
from datetime import datetime, timedelta

from test.support.utils import TestMixin, assert_401, assert_200


class TestStatisticsController(TestMixin):
    def test_registrations_for_unauthenticated(self, a_client):
        response = a_client.get('api/v1/statistics/registrations')

        assert_401(response)

    def test_registrations_returns_registrations_by_date(self, a_client, user_factory, a_client_user):
        user_factory()
        another_user = user_factory()
        another_user.created = datetime.now() + timedelta(days=1)
        another_user.save()

        self.login(a_client, a_client_user.email, a_client_user.password)
        response = self.get(a_client, 'api/v1/statistics/registrations')

        assert_200(response)

        data = json.loads(response.data)

        assert len(data) == 2
