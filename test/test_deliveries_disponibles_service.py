""" This module is the testing module for deliveries_disponibles_service """

import unittest
from unittest.mock import patch, MagicMock

from services.deliveries_disponibles_service import DeliveriesDisponiblesService
from models.delivery_disponible import DeliveryDisponible
from models.eliminar_delivery_disponible import EliminarDeliveryDisponible
from models.query_deliveries_cercanos import QueryDeliveriesCercanos

class DeliveriesDisponiblesServiceTestCase(unittest.TestCase):
    """ This class is the test case for deliveries_disponibles_service """

    #
    #   Success Tests
    #

    @patch('services.deliveries_disponibles_service.DB', autospec=True)
    def test_success_agregar_delivery(self, db_mock):
        """ Test success agregar delivery """
        # mocks
        db_mock.return_value = MagicMock()
        db_mock.encontrar_documento.return_value = None
        db_mock.agregar_documento.return_value = None

        service = DeliveriesDisponiblesService()
        ret_value = service.agregar_delivery_disponible(DeliveryDisponible(
            "1", "Santiago", "https://urlimagen.com", [-58.3772300, -34.6131500]))

        assert ret_value

    @patch('services.deliveries_disponibles_service.DB', autospec=True)
    def test_success_query_deliveries_cercanos(self, db_mock):
        """ Test success query deliveries cercanos """
        # mocks
        db_mock.return_value = MagicMock()
        db_mock.encontrar_lista_documentos.return_value = []

        service = DeliveriesDisponiblesService()
        ret_value = service.query_deliveries_cercanos(QueryDeliveriesCercanos(
            "5", [-58.3772300, -34.6131500]))

        assert ret_value == []

    @patch('services.deliveries_disponibles_service.DB', autospec=True)
    def test_success_eliminar_delivery(self, db_mock):
        """ Test success eliminar delivery """
        # mocks
        db_mock.return_value = MagicMock()
        db_mock.encontrar_documento.return_value = DeliveryDisponible(
            "1", "Santiago", "https://urlimagen.com", [-58.3772300, -34.6131500])
        db_mock.eliminar_documento.return_value = None

        service = DeliveriesDisponiblesService()
        ret_value = service.eliminar_delivery_disponible(EliminarDeliveryDisponible("1"))

        assert ret_value
