from unittest import mock, TestCase

from services.exceptions.unauthorized_user import UnauthorizedUserException


def function():
    pass


USER_DATA = {
    'email': 'user@email.com',
    'password': 'password'
}


class TestAuthService(TestCase):

    @mock.patch('services.auth_service.user_service')
    def test_validate_user(self, user_service):
        user_service.is_valid.return_value = False
        from services import auth_service

        with self.assertRaises(UnauthorizedUserException):
            auth_service.validate_user(USER_DATA)

    @mock.patch('services.auth_service.request')
    def test_authenticate_without_bearer(self, request):
        request.headers = {'Authorization': ''}
        from services import auth_service

        with self.assertRaises(UnauthorizedUserException):
            auth_service.authenticate(function)()

    @mock.patch('services.auth_service.request')
    @mock.patch('services.auth_service.user_service')
    def test_authenticate_without_valid_user(self, user_service, request):
        from services import jwt_service
        request.headers = {'Authorization': 'Bearer ' + jwt_service.encode_data_to_jwt(USER_DATA)}
        user_service.is_valid.return_value = False
        from services import auth_service

        with self.assertRaises(UnauthorizedUserException):
            auth_service.authenticate(function)()
