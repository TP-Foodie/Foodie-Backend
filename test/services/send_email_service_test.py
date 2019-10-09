from unittest import TestCase
from unittest.mock import Mock, patch


class SendEmailServiceTest(TestCase):

    @patch('services.send_email_service.SendGridAPIClient')
    def test_shoud_send_email(self, send_grid_api_client_mock):
        mock = Mock()
        send_grid_api_client_mock.return_value = mock

        from services import send_email_service
        send_email_service.send_token("email@foo.com", "token")

        self.assertTrue(mock.client.mail.send.post.called)
