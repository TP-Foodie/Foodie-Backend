import unittest
from unittest.mock import patch
import json

from app import APP, prefix
from deliveries_disponibles.models.delivery_disponible import DeliveryDisponible
from deliveries_disponibles.models.eliminar_delivery_disponible import EliminarDeliveryDisponible

mock_valid_delivery_disponible = {
    "_id": "1",
    "name": "Santiago",
    "profile_image": "https://urlimagen.com",
	"coordinates": [-58.3772300, -34.6131500]
}

mock_extra_field_delivery_disponible = {
    "_id": "1",
    "name": "Santiago",
	"profile_image": "https://urlimagen.com",
	"coordinates": [-58.3772300, -34.6131500],
    "extra_field": "extra"
}


class DeliveriesDisponiblesControllerTestCase(unittest.TestCase):
    def setUp(self):
        APP.config['TESTING'] = True
        self.app = APP.test_client()

    #
    #   Success Tests
    #

    @patch('deliveries_disponibles.services.deliveries_disponibles_service.DeliveriesDisponiblesService.agregar_delivery_disponible')
    def test_success_agregar_delivery(self, agregar_delivery_disponible_mock):
        agregar_delivery_disponible_mock.return_value = True
        response = self.app.post(
            f'{prefix}/deliveries_disponibles',
            data=json.dumps(mock_valid_delivery_disponible),
            content_type='application/json'
        )            

        assert response._status_code == 201

    @patch('deliveries_disponibles.services.deliveries_disponibles_service.DeliveriesDisponiblesService.eliminar_delivery_disponible')
    @patch('deliveries_disponibles.schemas.eliminar_delivery_disponible_schema.EliminarDeliveryDisponibleSchema')
    def test_success_eliminar_delivery(self, eliminar_delivery_disponible_mock, schema_mock):
        # mocks
        eliminar_delivery_disponible_mock.return_value = True
        schema_mock.load.return_value = EliminarDeliveryDisponible("1")

        response = self.app.delete(
            f'{prefix}/deliveries_disponibles',
            data=json.dumps({"_id": "1"}),
            content_type='application/json'
        )            

        assert response._status_code == 200


    #
    #   Wrong Tests
    #

    def test_wrong_extra_fields_agregar_delivery(self):
        response = self.app.post(
            f'{prefix}/deliveries_disponibles',
            data=json.dumps(mock_extra_field_delivery_disponible),
            content_type='application/json'
        )

        assert response._status_code == 400