""" This module is the testing module for deliveries_disponibles_service """

import unittest
from unittest.mock import patch, MagicMock

from services.available_deliveries_service import AvailableDeliveriesService
from models.available_delivery import AvailableDelivery
from models.delete_available_delivery import DeleteAvailableDelivery
from models.query_nearby_deliveries import QueryNearbyDeliveries

class DeliveriesDisponiblesServiceTestCase(unittest.TestCase):
    """ This class is the test case for deliveries_disponibles_service """

    #
    #   Success Tests
    #

    @patch('services.available_deliveries_service.DB', autospec=True)
    def test_success_agregar_delivery(self, db_mock):
        """ Test success agregar delivery """
        # mocks
        db_mock.return_value = MagicMock()
        db_mock.encontrar_documento.return_value = None
        db_mock.agregar_documento.return_value = None

        service = AvailableDeliveriesService()
        ret_value = service.add_available_delivery(AvailableDelivery(
            "1", "Santiago", "https://urlimagen.com", [-58.3772300, -34.6131500]))

        assert ret_value

    @patch('services.available_deliveries_service.DB', autospec=True)
    def test_success_query_deliveries_cercanos(self, db_mock):
        """ Test success query deliveries cercanos """
        # mocks
        db_mock.return_value = MagicMock()
        db_mock.encontrar_lista_documentos.return_value = []

        service = AvailableDeliveriesService()
        ret_value = service.query_nearby_deliveries(QueryNearbyDeliveries(
            "5", [-58.3772300, -34.6131500]))

        assert ret_value == []

    @patch('services.available_deliveries_service.DB', autospec=True)
    def test_success_eliminar_delivery(self, db_mock):
        """ Test success eliminar delivery """
        # mocks
        db_mock.return_value = MagicMock()
        db_mock.encontrar_documento.return_value = AvailableDelivery(
            "1", "Santiago", "https://urlimagen.com", [-58.3772300, -34.6131500])
        db_mock.eliminar_documento.return_value = None

        service = AvailableDeliveriesService()
        ret_value = service.delete_available_delivery(DeleteAvailableDelivery("1"))

        assert ret_value
