import json

from test.support.utils import assert_200


class TestOrderController:
    def test_orders_endpoint_exists(self, a_client):
        response = a_client.get('/orders/')
        assert_200(response)

    def test_list_orders(self, a_client, an_order):
        response = a_client.get('/orders/')
        order = json.loads(response.data)[0]
        assert order == {
            'id': str(an_order.id),
            'number': an_order.number,
            'status': an_order.status,
            'type': an_order.type,
        }
