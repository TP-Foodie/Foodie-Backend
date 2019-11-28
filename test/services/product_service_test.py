from test.support.utils import TestMixin
from services import product_service


class TestProductService(TestMixin):
    def test_get_products_from_place(self, a_client, a_client_user, a_product):
        self.login(a_client, a_client_user.email, a_client_user.password)
        products = product_service.get_products_from_place(a_product.place.id)
        assert products[0] == a_product
