""" This module is the testing module for deliveries_disponibles_controller """

import unittest
from unittest.mock import patch, MagicMock
import json
from marshmallow import ValidationError

from app import APP, PREFIX
from models.delivery_disponible import DeliveryDisponible
from models.query_deliveries_cercanos import QueryDeliveriesCercanos
from models.eliminar_delivery_disponible import EliminarDeliveryDisponible


class DeliveriesDisponiblesControllerTestCase(unittest.TestCase):
    """ This class is the test case for deliveries_disponibles_controller """
    def setUp(self):
        APP.config['TESTING'] = True
        self.app = APP.test_client()

    #
    #   Success Tests
    #

    @patch(
        'controllers.deliveries_disponibles_controller.DeliveriesDisponiblesService',
        autospec=True)
    @patch(
        'controllers.deliveries_disponibles_controller.DeliveryDisponibleSchema',
        autospec=True)
    def test_success_agregar_delivery(self, mock_schema, mock_service):
        """ Test success agregar delivery """
        # mocks
        mock_service.return_value = MagicMock()
        mock_service.agregar_delivery_disponible.return_value = True

        mock_schema.return_value = MagicMock()
        mock_schema.load.return_value = DeliveryDisponible(
            "1", "Santiago", "https://urlimagen.com", [-58.3772300, -34.6131500])

        # call controller
        response = self.app.post(
            f'{PREFIX}/deliveries_disponibles',
            data=json.dumps({
                "_id": "1", "name": "Santiago", "profile_image": \
                "https://urlimagen.com", "coordinates": [-58.3772300, -34.6131500]}),
            content_type='application/json')

        assert response._status_code == 201

    @patch(
        'controllers.deliveries_disponibles_controller.DeliveriesDisponiblesService',
        autospec=True)
    @patch(
        'controllers.deliveries_disponibles_controller.QueryDeliveriesCercanosSchema',
        autospec=True)
    def test_success_query_deliveries_cercanos(self, mock_schema, mock_service):
        """ Test success query deliveries cercanos """
        # mocks
        mock_service.return_value = MagicMock()
        mock_service.query_deliveries_cercanos.return_value = []

        mock_schema.return_value = MagicMock()
        mock_schema.load.return_value = QueryDeliveriesCercanos("5", [-58.3772300, -34.6131500])

        # call controller
        response = self.app.get(
            f'{PREFIX}/deliveries_disponibles',
            data=json.dumps({"radius": "5", "coordinates": [-58.3772300, -34.6131500]}),
            content_type='application/json')

        assert response._status_code == 200

    @patch(
        'controllers.deliveries_disponibles_controller.DeliveriesDisponiblesService',
        autospec=True)
    @patch(
        'controllers.deliveries_disponibles_controller.EliminarDeliveryDisponibleSchema',
        autospec=True)
    def test_success_eliminar_delivery(self, mock_schema, mock_service):
        """ Test success eliminar delivery """
        # mocks
        mock_service.return_value = MagicMock()
        mock_service.eliminar_delivery_disponible.return_value = True

        mock_schema.return_value = MagicMock()
        mock_schema.load.return_value = EliminarDeliveryDisponible("1")

        # call controller
        response = self.app.delete(
            f'{PREFIX}/deliveries_disponibles',
            data=json.dumps({"_id": "1"}),
            content_type='application/json')

        assert response._status_code == 200


    #
    #   Wrong Tests
    #

    @patch(
        'controllers.deliveries_disponibles_controller.DeliveryDisponibleSchema',
        autospec=True)
    def test_wrong_extra_fields_agregar_delivery(self, mock_schema):
        """ test wrong extra field in JSON al agregar delivery """
        # mocks
        mock_schema.return_value = MagicMock()
        mock_schema.side_effect = ValidationError("error message")

        response = self.app.post(
            f'{PREFIX}/deliveries_disponibles',
            data=json.dumps({
                "_id": "1", "name": "Santiago", "profile_image": \
                "https://urlimagen.com", "coordinates": [-58.3772300, -34.6131500],
                "extra_field": "extra"}),
            content_type='application/json')

        assert response._status_code == 400

    @patch('controllers.deliveries_disponibles_controller.DeliveryDisponibleSchema', autospec=True)
    def test_wrong_empty_id_agregar_delivery(self, mock_schema):
        """ test wrong empty id field in JSON al agregar delivery """
        # mocks
        mock_schema.return_value = MagicMock()
        mock_schema.side_effect = ValidationError("error message")

        response = self.app.post(
            f'{PREFIX}/deliveries_disponibles',
            data=json.dumps({
                "_id": "", "name": "Santiago", "profile_image": "https://urlimagen.com",
                "coordinates": [-58.3772300, -34.6131500]}),
            content_type='application/json'
        )

        assert response._status_code == 400

    @patch('controllers.deliveries_disponibles_controller.DeliveryDisponibleSchema', autospec=True)
    def test_wrong_empty_name_agregar_delivery(self, mock_schema):
        """ test wrong empty name field in JSON al agregar delivery """
        # mocks
        mock_schema.return_value = MagicMock()
        mock_schema.side_effect = ValidationError("error message")

        response = self.app.post(
            f'{PREFIX}/deliveries_disponibles',
            data=json.dumps({
                "_id": "1", "name": "", "profile_image": "https://urlimagen.com",
                "coordinates": [-58.3772300, -34.6131500]}),
            content_type='application/json')

        assert response._status_code == 400

    @patch('controllers.deliveries_disponibles_controller.DeliveryDisponibleSchema', autospec=True)
    def test_wrong_empty_profile_image_agregar_delivery(self, mock_schema):
        """ test wrong empty profile image field in JSON al agregar delivery """
        # mocks
        mock_schema.return_value = MagicMock()
        mock_schema.side_effect = ValidationError("error message")

        response = self.app.post(
            f'{PREFIX}/deliveries_disponibles',
            data=json.dumps({
                "_id": "1", "name": "Santiago", "profile_image": "",
                "coordinates": [-58.3772300, -34.6131500]}),
            content_type='application/json')

        assert response._status_code == 400

    @patch('controllers.deliveries_disponibles_controller.DeliveryDisponibleSchema', autospec=True)
    def test_wrong_empty_coordinates_agregar_delivery(self, mock_schema):
        """ test wrong empty coordinates field in JSON al agregar delivery """
        # mocks
        mock_schema.return_value = MagicMock()
        mock_schema.side_effect = ValidationError("error message")

        response = self.app.post(
            f'{PREFIX}/deliveries_disponibles',
            data=json.dumps({
                "_id": "1", "name": "Santiago", "profile_image": "https://urlimagen.com",
                "coordinates": []}),
            content_type='application/json')

        assert response._status_code == 400

    @patch('controllers.deliveries_disponibles_controller.DeliveryDisponibleSchema', autospec=True)
    def test_wrong_longitude_value_agregar_delivery(self, mock_schema):
        """ test wrong longitude value in coordinates field in JSON al agregar delivery """
        # mocks
        mock_schema.return_value = MagicMock()
        mock_schema.side_effect = ValidationError("error message")

        response = self.app.post(
            f'{PREFIX}/deliveries_disponibles',
            data=json.dumps({
                "_id": "1", "name": "Santiago", "profile_image": "https://urlimagen.com",
                "coordinates": [-190, -34.6131500]}),
            content_type='application/json')

        assert response._status_code == 400

    @patch('controllers.deliveries_disponibles_controller.DeliveryDisponibleSchema', autospec=True)
    def test_wrong_latitude_value_agregar_delivery(self, mock_schema):
        """ test wrong latitude value in coordinates field in JSON al agregar delivery """
        # mocks
        mock_schema.return_value = MagicMock()
        mock_schema.side_effect = ValidationError("error message")

        response = self.app.post(
            f'{PREFIX}/deliveries_disponibles',
            data=json.dumps({
                "_id": "1", "name": "Santiago", "profile_image": "https://urlimagen.com",
                "coordinates": [-58.3772300, -34.6131500]}),
            content_type='application/json')

        assert response._status_code == 400

    @patch('controllers.deliveries_disponibles_controller.DeliveryDisponibleSchema', autospec=True)
    def test_wrong_coordinates_length_agregar_delivery(self, mock_schema):
        """ test wrong length array in coordinates field in JSON al agregar delivery """
        # mocks
        mock_schema.return_value = MagicMock()
        mock_schema.side_effect = ValidationError("error message")

        response = self.app.post(
            f'{PREFIX}/deliveries_disponibles',
            data=json.dumps({
                "_id": "1", "name": "Santiago", "profile_image": "https://urlimagen.com",
                "coordinates": [-58.3772300, -34.6131500, 0]}),
            content_type='application/json')

        assert response._status_code == 400

    @patch('controllers.deliveries_disponibles_controller.DeliveryDisponibleSchema', autospec=True)
    def test_wrong_malfomed_image_url_agregar_delivery(self, mock_schema):
        """ test wrong malformed url in profile image field in JSON al agregar delivery """
        # mocks
        mock_schema.return_value = MagicMock()
        mock_schema.side_effect = ValidationError("error message")

        response = self.app.post(
            f'{PREFIX}/deliveries_disponibles',
            data=json.dumps({
                "_id": "1", "name": "Santiago", "profile_image": "urlimagen",
                "coordinates": [-58.3772300, -34.6131500]
            }),
            content_type='application/json')

        assert response._status_code == 400
