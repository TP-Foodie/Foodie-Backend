import unittest
from unittest.mock import patch, MagicMock

from app import APP, PREFIX
from deliveries_disponibles.services.deliveries_disponibles_service import DeliveriesDisponiblesService
from deliveries_disponibles.models.delivery_disponible import DeliveryDisponible
from deliveries_disponibles.models.eliminar_delivery_disponible import EliminarDeliveryDisponible
from deliveries_disponibles.models.query_deliveries_cercanos import QueryDeliveriesCercanos

class DeliveriesDisponiblesServiceTestCase(unittest.TestCase):
    def setUp(self):
        APP.config['TESTING'] = True
        self.app = APP.test_client()

    #
    #   Success Tests
    #

    @patch('deliveries_disponibles.services.deliveries_disponibles_service.DB', autospec=True)
    def test_success_agregar_delivery(self, db_mock):
        # mocks
        db_mock.return_value = MagicMock()
        db_mock.encontrar_documento.return_value = None
        db_mock.agregar_documento.return_value = None

        service = DeliveriesDisponiblesService()
        ret_value = service.agregar_delivery_disponible(DeliveryDisponible("1", "Santiago", "https://urlimagen.com", [-58.3772300, -34.6131500]))

        assert ret_value == True

    @patch('deliveries_disponibles.services.deliveries_disponibles_service.DB', autospec=True)
    def test_success_query_deliveries_cercanos(self, db_mock):
        # mocks
        db_mock.return_value = MagicMock()
        db_mock.encontrar_lista_documentos.return_value = []

        service = DeliveriesDisponiblesService()
        ret_value = service.query_deliveries_cercanos(QueryDeliveriesCercanos("5", [-58.3772300, -34.6131500]))

        assert ret_value == []

    @patch('deliveries_disponibles.services.deliveries_disponibles_service.DB', autospec=True)
    def test_success_eliminar_delivery(self, db_mock):
        # mocks
        db_mock.return_value = MagicMock()
        db_mock.encontrar_documento.return_value = DeliveryDisponible("1", "Santiago", "https://urlimagen.com", [-58.3772300, -34.6131500])
        db_mock.eliminar_documento.return_value = None

        service = DeliveriesDisponiblesService()
        ret_value = service.eliminar_delivery_disponible(EliminarDeliveryDisponible("1"))

        assert ret_value == True