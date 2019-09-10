import unittest
from unittest.mock import patch
import json

from app import APP, prefix
"""
mock_user = {
    "username": "realuser",
    "email": "realuser@real.com",
    "password": "password"
}

mock_login = {
    "username": "realuser",
    "password": "password"
}
"""

class DeliveriesDisponiblesControllerTestCase(unittest.TestCase):
    def setUp(self):
        APP.config['TESTING'] = True
        self.app = APP.test_client()

    def test_wrong_extra_fields_agregar_delivery(self):
        response = self.app.post(
            f'{prefix}/deliveries_disponibles',
            data=json.dumps({
                "_id": "1",
                "name": "Santiago",
	            "profile_image": "https://urlimagen.com",
	            "coordinates": [-58.3772300, -34.6131500],
                "extra_field": "extra"
            }),
            content_type='application/json'
        )

        assert response._status_code == 400

"""
    @patch('src.auth.services.auth_service.UserService.compare_password')
    def test_success_login(self, compare_password_mock):
        compare_password_mock.return_value = True
        with patch.object(UserService, 'get_user_by', return_value=copy.deepcopy(mock_user)):
            response = self.app.post(
                f'{prefix}/auth/login',
                data=json.dumps(mock_login),
                content_type='application/json'
            )
        assert response._status_code == 200

    def test_wrong_extra_fields_login(self):
        response = self.app.post(
            f'{prefix}/auth/login',
            data=json.dumps({
                "username": "realuser",
                "extra_field": "extra",
                "password": "password"
            }),
            content_type='application/json'
        )

        assert response._status_code == 400

    @patch('src.auth.services.auth_service.UserService.compare_password')
    def test_wrong_password_login(self, compare_password_mock):
        compare_password_mock.return_value = False
        with patch.object(UserService, 'get_user_by', return_value=copy.deepcopy(mock_user)):
            response = self.app.post(
                f'{prefix}/auth/login',
                data=json.dumps(mock_login),
                content_type='application/json'
            )
        assert response._status_code == 401

    def test_wrong_user_login(self):
        with patch.object(UserService, 'get_user_by', side_effect=UserNotFoundException("User not found")):
            response = self.app.post(
                f'{prefix}/auth/login',
                data=json.dumps(mock_login),
                content_type='application/json'
            )
        assert response._status_code == 401
"""