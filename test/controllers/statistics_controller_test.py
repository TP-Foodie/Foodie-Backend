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

    def test_completed_orders_for_unauthenticated(self, a_client):
        response = a_client.get('api/v1/statistics/completed_orders')

        assert_401(response)

    def test_list_completed_orders(self, a_client, a_client_user, a_complete_order):
        # pylint: disable=unused-argument
        self.login(a_client, a_client_user.email, a_client_user.password)
        response = self.get(a_client, 'api/v1/statistics/completed_orders')

        assert_200(response)

        orders = json.loads(response.data)

        assert orders[0]['count'] == 1

    def test_cancelled_orders_for_unauthenticated(self, a_client):
        response = a_client.get('api/v1/statistics/cancelled_orders')

        assert_401(response)

    def test_list_cancelled_orders(self, a_client, a_client_user, a_cancelled_order):
        # pylint: disable=unused-argument
        self.login(a_client, a_client_user.email, a_client_user.password)
        response = self.get(a_client, 'api/v1/statistics/cancelled_orders')

        assert_200(response)

        orders = json.loads(response.data)

        assert orders[0]['count'] == 1

    def test_list_registrations_in_specific_month(self, a_client, a_client_user, user_factory):
        user = user_factory()
        user.created = datetime.now() - timedelta(days=31)
        user.save()

        self.login(a_client, a_client_user.email, a_client_user.password)

        today = datetime.today()
        response = self.get(
            a_client,
            'api/v1/statistics/registrations?month={}&year={}'.format(today.month, today.year)
        )

        data = json.loads(response.data)

        assert len(data) == 1
        assert data[0]['count'] == 1
