from unittest import mock, TestCase

from services.exceptions.unauthorized_user import UnauthorizedUserException


def function():
    pass


class TestAuthService(TestCase):

    @mock.patch('src.services.auth_service.user_service')
    def test_validate_user(self, user_service):
        user_service.is_valid.return_value = False
        data = {
            'email': 'user@email.com',
            'password': 'password'
        }
        from src.services import auth_service

        with self.assertRaises(UnauthorizedUserException):
            auth_service.validate_user(data)

    @mock.patch('src.services.auth_service.request')
    def test_authenticate_without_bearer(self, request):
        request.headers = {'Authorization': ''}
        from src.services import auth_service

        with self.assertRaises(UnauthorizedUserException):
            auth_service.authenticate(function)()

    @mock.patch('src.services.auth_service.request')
    @mock.patch('src.services.auth_service.user_service')
    def test_authenticate_without_valid_user(self, request, user_service):
        request.headers = {'Authorization': 'Bearer asd'}
        user_service.is_valid.return_value = False
        from src.services import auth_service

        with self.assertRaises(UnauthorizedUserException):
            auth_service.authenticate(function)()
