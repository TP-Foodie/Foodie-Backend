from test.support.utils import assert_200


class TestOrderController:
    def test_orders_endpoint_exists(self, a_client):
        response = a_client.get('/orders/')
        assert_200(response)
