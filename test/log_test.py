from unittest import TestCase, mock
from unittest.mock import MagicMock


class LogTest(TestCase):

    @mock.patch('logger.request')
    @mock.patch('logger.current_app')
    def test_request_log(self, current_app, request):
        response = MagicMock()

        def function():
            return response

        import logger
        logger.log_request_response(function)()

        self.assertTrue(request.json.__str__.called)
        self.assertTrue(response.json.__str__.called)
        self.assertTrue(current_app.logger.info.called)
