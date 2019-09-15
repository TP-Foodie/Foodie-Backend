import json

from test.support.utils import assert_200


class TestOrderController:
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