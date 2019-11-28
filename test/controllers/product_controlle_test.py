import json
import urllib

from test.support.utils import TestMixin, assert_200


class TestProductController(TestMixin):
    def build_url(self, url):
        return f'/api/v1{url}'

    def get_products_by_place(self, client, a_client_user, id_place):
        self.login(client, a_client_user.email, a_client_user.password)
        params = {'id_place': id_place}
        url = 'api/v1/products/?' + urllib.parse.urlencode(params)
        return self.get(client, url)

    def test_get_products_by_place(self, a_client, a_client_user, a_product):
        response = self.get_products_by_place(a_client, a_client_user, a_product.place.id)

        assert_200(response)

        products = json.loads(response.data)
        assert products[0] == {
            'id': str(a_product.id),
            'name': a_product.name,
            'description': a_product.description,
            'image': a_product.image,
            'price': a_product.price,
            'place': {
                'id': str(a_product.place.id),
                'name': a_product.place.name,
                'image': a_product.place.image,
                'coordinates': {
                    'latitude': a_product.place.coordinates.latitude,
                    'longitude': a_product.place.coordinates.longitude
                }
            }
        }
