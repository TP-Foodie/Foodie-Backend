import json

from src.models.order import Order
from src.repositories import order_repository
from test.support.utils import assert_200, assert_201, assert_400


class TestOrderController:
    def get_favor_orders(self, client):
        return client.get('/orders/favors')

    def create_order(self, client, order_type, user, product):
        return client.post('/orders/',
                           json={
                               'order_type': order_type,
                               'owner': user.id,
                               'product': {
                                   'name': product.name,
                                   'place': product.place.id
                               }
                           })

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
            },
            'product': {
                'name': an_order.product.name,
                'place': {
                    'name': an_order.product.place.name,
                    'coordinates': {
                        'latitude': an_order.product.place.coordinates.latitude,
                        'longitude': an_order.product.place.coordinates.longitude
                    }
                }
            }
        }

    def test_get_orders_filtered_by_favors(self, a_client, a_favor_order, an_order_factory):
        an_order_factory()
        response = self.get_favor_orders(a_client)

        assert_200(response)

        orders = json.loads(response.data)

        assert len(orders) == 1
        assert orders[0]['id'] == str(a_favor_order.id)

    def test_user_should_be_able_to_create_order(self, a_client, a_client_user, a_product):
        response = self.create_order(a_client, Order.NORMAL_TYPE, a_client_user, a_product)
        assert_201(response)

    def test_create_orders_should_create_one_on_db(self, a_client, a_client_user, a_product):
        self.create_order(a_client, Order.NORMAL_TYPE, a_client_user, a_product)

        assert len(order_repository.list_all()) == 1

    def test_create_should_return_created_http_code(self, a_client, a_client_user, a_product):
        response = self.create_order(a_client, Order.NORMAL_TYPE, a_client_user, a_product)
        assert_201(response)

    def test_create_with_wrong_type_should_return_400(self, a_client, a_client_user, a_product):
        response = self.create_order(a_client, "NONEXISTINGTYPE", a_client_user, a_product)
        assert_400(response)

    def test_create_with_non_existing_place_should_return_400(self, a_client, a_client_user, a_product):
        a_product.place.id = 1
        response = self.create_order(a_client, "NONEXISTINGTYPE", a_client_user, a_product)
        assert_400(response)