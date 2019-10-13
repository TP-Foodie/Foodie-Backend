from unittest import mock


class TestJwtService:

    @mock.patch('settings.Config')
    def test_jwt_service(self, config):
        config.JWT_SECRET.return_value = 'jwt_secret'
        data = {
            'email': 'user@mail.com',
            'password': 'password'
        }

        from services import jwt_service
        encoded_data = jwt_service.encode_data_to_jwt(data)

        assert jwt_service.decode_jwt_data(encoded_data) == data
