import unittest
from unittest.mock import patch, MagicMock
from repositories import messaging_repository


class TestMessagingRepository(unittest.TestCase):

    def test_empty_registration_token(self):
        response = messaging_repository.send_message_to_device("message", "")
        assert not response

    @patch('repositories.messaging_repository.Message')
    @patch('repositories.messaging_repository.send')
    def test_normal_registration_token(self, mock_send, mock_message):
        mock_message.return_value = MagicMock()
        mock_send.return_value = "OK"
        response = messaging_repository.send_message_to_device({}, "token")

        assert response
