""" This module is the testing module for available deliveries controller """

import unittest
from unittest.mock import patch, MagicMock

from app import APP, PREFIX
from controllers.available_deliveries_controller import AVAILABLE_DELIVERIES_ROUTE
from models import User


class DeliveriesDisponiblesControllerTestCase(unittest.TestCase):
    """ This class is the test case for available deliveries controller """

    def setUp(self):
        APP.config['TESTING'] = True
        self.app = APP.test_client()

    #
    #   Success Tests
    #

    @patch(
        'controllers.available_deliveries_controller.available_deliveries_service',
        autospec=True)
    def test_success_query_nearby_deliveries(self, mock_service):
        """ Test success query nearby deliveries """
        # mocks
        mock_service.return_value = MagicMock()
        mock_service.query_nearby_deliveries.return_value = [User(
            "1", "Santiago", "https://urlimagen.com", [-58.3772300, -34.6131500])]

        # call controller
        params = "?radius=5&latitude=-58.3772300&longitude=-34.6131500"
        response = self.app.get(f'{PREFIX}/' + AVAILABLE_DELIVERIES_ROUTE + params,
                                content_type='application/json')

        assert response.status_code == 200
