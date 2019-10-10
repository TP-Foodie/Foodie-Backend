from unittest import mock, TestCase

from mongoengine import DoesNotExist

from services.exceptions.unauthorized_user import UnauthorizedUserException


def function():
    pass


USER_DATA = {
    'email': 'user@email.com',
    'password': 'password'
}

USER_DATA_GOOGLE_AUDIENCE = {
    'aud': '218514362361-nchqu6j59rcskl1vmadfp6gl6ud8a0oo.apps.googleusercontent.com',
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
        request.headers = {
            'Authorization': 'Bearer ' + jwt_service.encode_data_to_jwt(USER_DATA_GOOGLE_AUDIENCE)}
        user_service.is_valid.return_value = False
        from services import auth_service

        with self.assertRaises(UnauthorizedUserException):
            auth_service.authenticate(function)()

    @mock.patch('services.auth_service.request')
    @mock.patch('services.auth_service.jwt_service')
    @mock.patch('services.auth_service.user_service')
    def test_authenticate_valid_google__user(self, user_service, jwt_service, request):
        request.headers = {'Authorization': 'Bearer xxx'}
        jwt_service.decode_jwt_data.return_value = {'sub': 'asd'}
        user_service.is_valid.return_value = True

        from services import auth_service

        auth_service.authenticate(function)()

    @mock.patch('services.auth_service.request')
    @mock.patch('services.auth_service.jwt_service')
    @mock.patch('services.auth_service.user_service')
    def test_authenticate_valid_user(self, user_service, jwt_service, request):
        request.headers = {'Authorization': 'Bearer xxx'}
        jwt_service.decode_jwt_data.return_value = {'email': 'asd', 'password': 'asd'}
        user_service.is_valid.return_value = True

        from services import auth_service

        auth_service.authenticate(function)()

    @mock.patch('services.auth_service.id_token')
    @mock.patch('services.auth_service.user_service')
    def test_validate_google_user(self, user_service, id_token):
        id_token.verify_oauth2_token.return_value = {
            'iss': 'accounts.google.com', 'email': 'foo@foo.foo'}
        user_service.get_user_by_email.return_value = "user"

        from services import auth_service

        assert auth_service.validate_google_user({'google_token': 'asd'})

    @mock.patch('services.auth_service.id_token')
    @mock.patch('services.auth_service.user_service')
    def test_validate_google_user_with_creation(self, user_service, id_token):
        id_token.verify_oauth2_token.return_value = {
            'iss': 'accounts.google.com', 'email': 'foo@foo.foo'}
        user_service.get_user_by_email.side_effect = DoesNotExist

        from services import auth_service

        auth_service.validate_google_user({'google_token': 'asd'})

        self.assertTrue(user_service.create_user_from_google_data.called)

    @mock.patch('services.auth_service.user_service')
    @mock.patch('services.auth_service.send_email_service')
    def test_new_token(self, send_email_service_mock, user_service_mock):
        from services import auth_service
        auth_service.generate_and_send_token({"email": "foo@foo.foo"})

        self.assertTrue(send_email_service_mock.send_token.called)
        self.assertTrue(user_service_mock.set_recovery_token.called)

    @mock.patch('services.auth_service.user_service')
    def test_update_password(self, user_service_mock):
        from services import auth_service
        auth_service.update_password({})

        self.assertTrue(user_service_mock.verify_user_token.called)
        self.assertTrue(user_service_mock.update_user_password.called)
