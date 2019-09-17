""" This module is the testing module for available deliveries controller """

import unittest
from unittest.mock import patch, MagicMock
import json

from app import APP, PREFIX
from controllers.available_deliveries_controller import AVAILABLE_DELIVERIES_ROUTE
from models.available_delivery import AvailableDelivery
from models.query_nearby_deliveries import QueryNearbyDeliveries


class DeliveriesDisponiblesControllerTestCase(unittest.TestCase):
    """ This class is the test case for available deliveries controller """
    def setUp(self):
        APP.config['TESTING'] = True
        self.app = APP.test_client()

    #
    #   Success Tests
    #

    @patch(
        'controllers.available_deliveries_controller.AvailableDeliveriesService',
        autospec=True)
    def test_success_add_delivery(self, mock_service):
        """ Test success add delivery as available """
        # mocks
        mock_service.return_value = MagicMock()
        mock_service.add_available_delivery.return_value = True

        # call controller
        response = self.app.post(
            f'{PREFIX}/' + AVAILABLE_DELIVERIES_ROUTE,
            data=json.dumps({
                "_id": "1", "name": "Santiago", "profile_image": \
                "https://urlimagen.com", "coordinates": [-58.3772300, -34.6131500]}),
            content_type='application/json')

        assert response._status_code == 201

    @patch(
        'controllers.available_deliveries_controller.AvailableDeliveriesService',
        autospec=True)
    def test_success_query_nearby_deliveries(self, mock_service):
        """ Test success query nearby deliveries """
        # mocks
        mock_service.return_value = MagicMock()
        mock_service.query_nearby_deliveries.return_value = [AvailableDelivery(
            "1", "Santiago", "https://urlimagen.com", [-58.3772300, -34.6131500])]

        # call controller
        response = self.app.get(
            f'{PREFIX}/' + AVAILABLE_DELIVERIES_ROUTE,
            data=json.dumps({"radius": "5", "coordinates": [-58.3772300, -34.6131500]}),
            content_type='application/json')

        assert response._status_code == 200

    @patch(
        'controllers.available_deliveries_controller.AvailableDeliveriesService',
        autospec=True)
    def test_success_delete_delivery(self, mock_service):
        """ Test success delete delivery as available """
        # mocks
        mock_service.return_value = MagicMock()
        mock_service.delete_available_delivery.return_value = True

        # call controller
        response = self.app.delete(
            f'{PREFIX}/' + AVAILABLE_DELIVERIES_ROUTE,
            data=json.dumps({"_id": "1"}),
            content_type='application/json')

        assert response._status_code == 200


    #
    #   Wrong Tests
    #

    def test_wrong_extra_fields_add_delivery(self):
        """ test wrong extra field in JSON while adding delivery as available """
        response = self.app.post(
            f'{PREFIX}/' + AVAILABLE_DELIVERIES_ROUTE,
            data=json.dumps({
                "id": "1", "name": "Santiago", "profile_image": \
                "https://urlimagen.com", "coordinates": [-58.3772300, -34.6131500],
                "extra_field": "extra"}),
            content_type='application/json')

        assert response._status_code == 400

    def test_wrong_empty_id_agregar_delivery(self):
        """ test wrong empty id field in JSON while adding delivery as available """
        response = self.app.post(
            f'{PREFIX}/' + AVAILABLE_DELIVERIES_ROUTE,
            data=json.dumps({
                "id": "", "name": "Santiago", "profile_image": "https://urlimagen.com",
                "coordinates": [-58.3772300, -34.6131500]}),
            content_type='application/json'
        )

        assert response._status_code == 400

    def test_wrong_empty_name_agregar_delivery(self):
        """ test wrong empty name field in JSON while adding delivery as available """
        response = self.app.post(
            f'{PREFIX}/' + AVAILABLE_DELIVERIES_ROUTE,
            data=json.dumps({
                "id": "1", "name": "", "profile_image": "https://urlimagen.com",
                "coordinates": [-58.3772300, -34.6131500]}),
            content_type='application/json')

        assert response._status_code == 400

    def test_wrong_empty_profile_image_agregar_delivery(self):
        """ test wrong empty profile image field in JSON while adding delivery as available """
        response = self.app.post(
            f'{PREFIX}/' + AVAILABLE_DELIVERIES_ROUTE,
            data=json.dumps({
                "id": "1", "name": "Santiago", "profile_image": "",
                "coordinates": [-58.3772300, -34.6131500]}),
            content_type='application/json')

        assert response._status_code == 400

    def test_wrong_empty_coordinates_agregar_delivery(self):
        """ test wrong empty coordinates field in JSON while adding delivery as available """
        response = self.app.post(
            f'{PREFIX}/' + AVAILABLE_DELIVERIES_ROUTE,
            data=json.dumps({
                "id": "1", "name": "Santiago", "profile_image": "https://urlimagen.com",
                "coordinates": []}),
            content_type='application/json')

        assert response._status_code == 400

    def test_wrong_longitude_value_agregar_delivery(self):
        """ test wrong longitude value in coordinates field in JSON while adding delivery as available """
        response = self.app.post(
            f'{PREFIX}/' + AVAILABLE_DELIVERIES_ROUTE,
            data=json.dumps({
                "id": "1", "name": "Santiago", "profile_image": "https://urlimagen.com",
                "coordinates": [-190, -34.6131500]}),
            content_type='application/json')

        assert response._status_code == 400

    def test_wrong_latitude_value_agregar_delivery(self):
        """ test wrong latitude value in coordinates field in JSON while adding delivery as available """
        response = self.app.post(
            f'{PREFIX}/' + AVAILABLE_DELIVERIES_ROUTE,
            data=json.dumps({
                "id": "1", "name": "Santiago", "profile_image": "https://urlimagen.com",
                "coordinates": [-58.3772300, -34.6131500]}),
            content_type='application/json')

        assert response._status_code == 400

    def test_wrong_coordinates_length_agregar_delivery(self):
        """ test wrong length array in coordinates field in JSON while adding delivery as available """
        response = self.app.post(
            f'{PREFIX}/' + AVAILABLE_DELIVERIES_ROUTE,
            data=json.dumps({
                "id": "1", "name": "Santiago", "profile_image": "https://urlimagen.com",
                "coordinates": [-58.3772300, -34.6131500, 0]}),
            content_type='application/json')

        assert response._status_code == 400

    def test_wrong_malfomed_image_url_agregar_delivery(self):
        """ test wrong malformed url in profile image field in JSON while adding delivery as available """
        response = self.app.post(
            f'{PREFIX}/' + AVAILABLE_DELIVERIES_ROUTE,
            data=json.dumps({
                "id": "1", "name": "Santiago", "profile_image": "urlimagen",
                "coordinates": [-58.3772300, -34.6131500]
            }),
            content_type='application/json')

        assert response._status_code == 400
