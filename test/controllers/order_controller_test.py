import json

from src.models.order import Order
from test.support.utils import assert_200


class TestOrderController:
    def get_favor_orders(self, client):
        return client.get('/orders/favors')

    def get_orders(self, client):
        return client.get('/orders/')

    def get_order(self, client, order_id):
        return client.get('/orders/{}'.format(str(order_id)))

    def test_orders_endpoint_exists(self, a_client):
        response = self.get_orders(a_client)
        assert_200(response)

    def test_list_orders(self, a_client, an_order):
        response = self.get_orders(a_client)
        order = json.loads(response.data)[0]

        assert order == {
            'id': str(an_order.id),
            'number': an_order.number,
            'status': an_order.status,
            'type': an_order.type,
        }

    def test_get_order_details(self, a_client, an_order):
        response = self.get_order(a_client, an_order.id)

        assert_200(response)

        order = json.loads(response.data)

        assert order == {
            'id': str(an_order.id),
            'number': an_order.number,
            'status': an_order.status,
            'type': an_order.type,
            'owner': {
                'name': an_order.owner.name,
                'last_name': an_order.owner.last_name,
                'email': an_order.owner.email,
                'profile_image': an_order.owner.profile_image,
                'phone': an_order.owner.phone
            }
        }

    def test_get_orders_filtered_by_favors(self, a_client, a_favor_order, an_order_factory):
        an_order_factory()
        response = self.get_favor_orders(a_client)

        assert_200(response)

        orders = json.loads(response.data)

        assert len(orders) == 1
        assert orders[0]['id'] == str(a_favor_order.id)
