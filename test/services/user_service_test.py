from unittest import mock
from unittest.mock import Mock, MagicMock

MOCK_OBJECT = Mock()


class TestUserService:

    @mock.patch('services.user_service.User')
    def test_get_users(self, mock_user):
        users = ['user1', 'user2']
        mock_user.objects = MOCK_OBJECT
        mock_skip = Mock()
        MOCK_OBJECT.skip.return_value = mock_skip
        mock_skip.limit.return_value = users

        from src.services import user_service

        assert users == user_service.get_users(0, 10)

    @mock.patch('services.user_service.User')
    def test_get_user(self, mock_user):
        user = "user"
        mock_user.objects = MOCK_OBJECT
        MOCK_OBJECT.get.return_value = user

        from src.services import user_service

        assert user == user_service.get_user(1)

    @mock.patch('services.user_service.User')
    def test_create_user(self, mock_user):
        user = {"id": 1}
        new_user = MagicMock()
        new_user.save.return_value = user
        mock_user.return_value = new_user

        from src.services import user_service
        assert user_service.create_user(user) == user

    @mock.patch('services.user_service.User')
    def test_update_user(self, mock_user):
        old_user = MagicMock()
        mock_user.get.return_value = old_user
        old_user.save.return_value = True

        from src.services import user_service
        assert user_service.update_user(1, {"name": "nombre"})
