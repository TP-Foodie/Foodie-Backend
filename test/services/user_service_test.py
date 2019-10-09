import hashlib
from datetime import timedelta, datetime
from unittest import mock, TestCase
from unittest.mock import Mock, MagicMock

from services.exceptions.unauthorized_user import UnauthorizedUserException

MOCK_OBJECT = Mock()


class TestUserService(TestCase):

    @mock.patch('services.user_service.User')
    def test_get_users_should_return_users(self, mock_user):
        users = ['user1', 'user2']
        mock_user.objects = MOCK_OBJECT
        mock_skip = Mock()
        MOCK_OBJECT.skip.return_value = mock_skip
        mock_skip.limit.return_value = users

        from services import user_service

        assert users == user_service.get_users(0, 10)

    @mock.patch('services.user_service.User')
    def test_get_user_should_return_user(self, mock_user):
        user = "user"
        mock_user.objects.get.return_value = user

        from services import user_service

        assert user == user_service.get_user(1)

    @mock.patch('services.user_service.User')
    def test_create_user_should_create_user(self, mock_user):
        user = {"id": 1}
        new_user = MagicMock()
        new_user.save.return_value = user
        mock_user.return_value = new_user

        from services import user_service
        assert user_service.create_user(user) == user

    @mock.patch('services.user_service.User')
    def test_update_user_should_update_user(self, mock_user):
        old_user = MagicMock()
        mock_user.get.return_value = old_user
        old_user.save.return_value = True

        from services import user_service
        assert user_service.update_user(1, {"name": "nombre"})

    @mock.patch('services.user_service.User')
    def test_is_valid_user_should_verify_user_with_password(self, mock_user):
        current_user = MagicMock()
        current_user.password = hashlib.md5("password".encode('utf-8')).hexdigest()
        mock_user.objects.get.return_value = current_user

        from services import user_service
        assert user_service.is_valid(email="email@email.com", password="password")

    @mock.patch('services.user_service.User')
    def test_is_valid_user_should_not_verify_user_with_wrong_password(self, mock_user):
        current_user = MagicMock()
        current_user.password = hashlib.md5("".encode('utf-8')).hexdigest()
        mock_user.objects.get.return_value = current_user

        from services import user_service
        assert not user_service.is_valid(email="email@email.com", password="password")

    @mock.patch('services.user_service.User')
    def test_is_valid_user_should_verify_user_with_google_id(self, mock_user):
        current_user = MagicMock()
        mock_user.objects.get.return_value = current_user

        from services import user_service
        assert user_service.is_valid(google_id="asd")

    @mock.patch('services.user_service.User')
    def test_token_not_matching_should_raise_exception(self, mock_user):
        current_user = MagicMock()
        mock_user.objects.get.return_value = current_user
        current_user.recovery_token = 'un_token'

        from services import user_service
        with self.assertRaises(UnauthorizedUserException):
            user_service.verify_user_token(
                {
                    'email': 'foo@foo.foo',
                    'recovery_token': 'recovery_token'
                }
            )

    @mock.patch('services.user_service.User')
    def test_token_out_of_date_should_raise_exception(self, mock_user):
        current_user = MagicMock()
        mock_user.objects.get.return_value = current_user
        current_user.recovery_token = 'recovery_token'
        current_user.recovery_token_date = datetime.utcnow() - timedelta(days=2)

        from services import user_service
        with self.assertRaises(UnauthorizedUserException):
            user_service.verify_user_token(
                {
                    'email': 'foo@foo.foo',
                    'recovery_token': 'recovery_token'
                }
            )

    @mock.patch('services.user_service.User')
    def test_update_password(self, mock_user):
        current_user = MagicMock()
        mock_user.objects.get.return_value = current_user

        from services import user_service
        user_service.update_user_password({
            'email': 'foo@foo.foo',
            'password': 'asd'
        })

        assert current_user.password == hashlib.md5('asd'.encode('utf-8')).hexdigest()
