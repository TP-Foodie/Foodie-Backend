import hashlib
from datetime import timedelta, datetime
from unittest import mock, TestCase
from unittest.mock import Mock, MagicMock

import pytest
from services.exceptions.unauthorized_user import UnauthorizedUserException
from services import user_service

MOCK_OBJECT = Mock()


class TestUserService(TestCase):

    @mock.patch('services.user_service.User')
    def test_get_users_should_return_users(self, mock_user):
        users = ['user1', 'user2']
        mock_user.objects = MOCK_OBJECT
        mock_skip = Mock()
        MOCK_OBJECT.skip.return_value = mock_skip
        mock_skip.limit.return_value = users

        assert users == user_service.get_users(0, 10)

    @mock.patch('services.user_service.User')
    def test_get_user_should_return_user(self, mock_user):
        user = "user"
        mock_user.objects.get.return_value = user

        assert user == user_service.get_user(1)

    @mock.patch('services.user_service.User')
    def test_create_user_should_create_user(self, mock_user):
        user = {"id": 1}
        new_user = MagicMock()
        new_user.save.return_value = user
        mock_user.return_value = new_user

        assert user_service.create_user(user) == user

    @mock.patch('services.user_service.User')
    def test_update_user_should_update_user(self, mock_user):
        old_user = MagicMock()
        mock_user.get.return_value = old_user
        old_user.save.return_value = True

        assert user_service.update_user(1, {"name": "nombre"})

    @mock.patch('services.user_service.User')
    def test_is_valid_user_should_verify_user_with_password(self, mock_user):
        current_user = MagicMock()
        current_user.password = hashlib.md5("password".encode('utf-8')).hexdigest()
        mock_user.objects.get.return_value = current_user

        assert user_service.is_valid(email="email@email.com", password="password")

    @mock.patch('services.user_service.User')
    def test_is_valid_user_should_not_verify_user_with_wrong_password(self, mock_user):
        current_user = MagicMock()
        current_user.password = hashlib.md5("".encode('utf-8')).hexdigest()
        mock_user.objects.get.return_value = current_user

        assert not user_service.is_valid(email="email@email.com", password="password")

    @mock.patch('services.user_service.User')
    def test_is_valid_user_should_verify_user_with_google_id(self, mock_user):
        current_user = MagicMock()
        mock_user.objects.get.return_value = current_user

        assert user_service.is_valid(google_id="asd")

    @mock.patch('services.user_service.User')
    def test_token_not_matching_should_raise_exception(self, mock_user):
        current_user = MagicMock()
        mock_user.objects.get.return_value = current_user
        current_user.recovery_token = 'un_token'

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

        user_service.update_user_password({
            'email': 'foo@foo.foo',
            'password': 'asd'
        })

        assert current_user.password == hashlib.md5('asd'.encode('utf-8')).hexdigest()


@pytest.mark.usefixtures('a_client')
class TestUserVariables:
    def test_user_daily_travels_returns_user_order_count(self, a_delivery_user, an_order):
        an_order.delivery = a_delivery_user
        an_order.save()

        assert user_service.daily_travels(a_delivery_user) == 1

    def test_user_daily_travels_returns_zero_if_today_did_not_travel(self,
                                                                     a_delivery_user,
                                                                     an_order):
        an_order.delivery = a_delivery_user
        an_order.date = datetime.today() - timedelta(days=1)  # yesterday
        an_order.save()

        assert user_service.daily_travels(a_delivery_user) == 0

    def test_user_daily_travels_returns_right_amount(self, a_delivery_user, an_order_factory):
        an_order = an_order_factory()
        another_order = an_order_factory()

        an_order.delivery = a_delivery_user
        an_order.date = datetime.today() - timedelta(days=1)  # yesterday
        an_order.save()

        another_order.delivery_user = a_delivery_user
        another_order.date = datetime.today()
        another_order.save()

        assert user_service.daily_travels(a_delivery_user) == 1

    def test_user_monthly_travels_returns_travels_made_in_month(self, an_order, a_delivery_user):
        an_order.delivery = a_delivery_user
        an_order.save()

        assert user_service.monthly_travels(a_delivery_user) == 1

    def test_user_monthly_travels_returns_zero_if_no_travels(self, a_delivery_user):
        assert user_service.monthly_travels(a_delivery_user) == 0

    def test_user_monthly_travels_returns_zero_if_travel_was_on_past_month(self,
                                                                           an_order,
                                                                           a_delivery_user):
        an_order.delivery = a_delivery_user
        an_order.date = datetime.today().date() - timedelta(days=30)
        an_order.save()

        assert user_service.monthly_travels(a_delivery_user) == 0

    def test_user_antiquity_returns_zero_if_created_today(self, a_customer_user):
        a_customer_user.created = datetime.now().date()

        assert user_service.antiquity(a_customer_user) == 0

    def test_user_antiquity_returns_antiquity_in_days(self, a_customer_user):
        a_customer_user.created = datetime.now().date() - timedelta(days=1)

        assert user_service.antiquity(a_customer_user) == 1
