import json

from test.support.utils import assert_200, assert_201, assert_400, assert_404, TestMixin, assert_401
from models.order import Order
from repositories import order_repository


class TestOrderController(TestMixin):  # pylint: disable=too-many-public-methods
    def build_url(self, url):
        return f'/api/v1{url}'

    def patch_order(self, client, order, user, data):
        self.login(client, user.email, user.password)
        return self.patch(
            client,
            self.build_url('/orders/{}'.format(str(order.id))),
            data
        )

    def get_favor_orders(self, client, user):
        self.login(client, user.email, user.password)
        return self.get(client, self.build_url('/orders/favors'))

    def create_order(self, client, order_type, user, product):
        self.login(client, user.email, user.password)
        return self.post(
            client,
            self.build_url('/orders/'),
            {
                'order_type': order_type,
                'product': {
                    'name': product.name,
                    'place': product.place.id
                }
            })

    def get_orders(self, client, user):
        self.login(client, user.email, user.password)
        return self.get(client, self.build_url('/orders/'))

    def get_order(self, client, order_id, a_client_user):
        self.login(client, a_client_user.email, a_client_user.password)
        return self.get(client, self.build_url('/orders/{}'.format(str(order_id))))

    def test_orders_endpoint_exists(self, a_client, a_client_user):
        response = self.get_orders(a_client, a_client_user)
        assert_200(response)

    def test_list_orders_for_unauthenticated(self, a_client):
        response = a_client.get(self.build_url('/orders/'))
        assert_401(response)

    def test_list_orders(self, a_client, an_order, a_client_user):
        response = self.get_orders(a_client, a_client_user)
        order = json.loads(response.data)[0]

        assert order == {
            'id': str(an_order.id),
            'number': an_order.number,
            'status': an_order.status,
            'type': an_order.type,
        }

    def test_get_orders_details_for_unauthenticated(self, a_client, an_order):
        response = a_client.get('api/v1/orders/{}'.format(str(an_order.id)))
        assert_401(response)

    def test_get_order_details(self, a_client, an_order, a_client_user):
        response = self.get_order(a_client, an_order.id, a_client_user)

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

    def test_get_orders_filtered_by_favors_for_unauthenticated(self, a_client):
        response = a_client.get('api/v1/orders/favors')
        assert_401(response)

    def test_get_orders_filtered_by_favors(self, a_client, a_favor_order,
                                           an_order_factory, a_client_user):
        an_order_factory()
        response = self.get_favor_orders(a_client, a_client_user)

        assert_200(response)

        orders = json.loads(response.data)

        assert len(orders) == 1
        assert orders[0]['id'] == str(a_favor_order.id)

    def test_create_for_unauthenticated(self, a_client):
        response = a_client.post('api/v1/orders/', json={})
        assert_401(response)

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

    def test_create_with_invalid_place_id_should_return_400(
            self, a_client, a_client_user, a_product):
        a_product.place.id = '1'
        response = self.create_order(a_client, Order.NORMAL_TYPE, a_client_user, a_product)
        assert_400(response)

    def test_update_for_unauthenticated(self, a_client, an_order):
        response = a_client.patch('api/v1/orders/{}'.format(str(an_order.id)), json={})
        assert_401(response)

    def test_update_should_change_order_status(self, a_client, an_order,
                                               a_delivery_user, a_client_user):
        response = self.patch_order(
            a_client,
            an_order,
            a_client_user,
            {'status': Order.TAKEN_STATUS, 'delivery': str(a_delivery_user.id)}
        )

        assert_200(response)

        assert order_repository.get_order(an_order.id).status == Order.TAKEN_STATUS

    def test_should_return_400_if_delivery_does_not_exists(self, a_client, an_object_id,
                                                           an_order, a_client_user):
        response = self.patch_order(
            a_client, an_order,
            a_client_user,
            {'status': Order.TAKEN_STATUS, 'delivery': str(an_object_id)}
        )

        assert_400(response)

    def test_should_return_404_if_order_does_not_exists(self, a_client, an_object_id,
                                                        a_delivery_user, a_client_user):
        self.login(a_client, a_client_user.email, a_client_user.password)
        response = self.patch(
            a_client,
            'orders/{}'.format(str(an_object_id)),
            {'status': Order.TAKEN_STATUS, 'delivery': str(a_delivery_user.id)},
        )

        assert_404(response)
