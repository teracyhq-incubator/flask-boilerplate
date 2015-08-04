# -*- coding: utf-8 -*-

"""tests for api_1_0.errors"""

from mock import MagicMock, patch

from tests.unit import UnitTestCase
from app.api_1_0.errors import api_exception_handler, error_handler


class ErrorsTestCase(UnitTestCase):

    @patch('app.api_1_0.errors.api_exception_handler')
    def test_value_error_handler(self, mock_api_exception_handler):

        from app.api_1_0.errors import value_error_handler

        mock_error = MagicMock()

        value_error_handler(mock_error)
        self.assertEqual(mock_api_exception_handler.call_count, 1)

    @patch('app.api_1_0.errors.api_exception_handler')
    def test_sql_alchemy_error_handler(self, mock_api_exception_handler):

        from app.api_1_0.errors import sql_alchemy_error_handler

        mock_error = MagicMock()

        sql_alchemy_error_handler(mock_error)
        self.assertEqual(mock_api_exception_handler.call_count, 1)

    @patch('app.api_1_0.errors.api_exception_handler')
    def test_invalid_token_error_handler(self, mock_api_exception_handler):
        from app.api_1_0.errors import invalid_token_error_handler

        mock_error = MagicMock()

        invalid_token_error_handler(mock_error)
        self.assertEqual(mock_api_exception_handler.call_count, 1)

    @patch('app.api_1_0.errors.NotFoundException')
    @patch('app.api_1_0.errors.render_template')
    @patch('app.api_1_0.errors.api_exception_handler')
    @patch('app.api_1_0.errors.request')
    def test_error_handler(self, mock_request, mock_api_exception_handler, mock_render_template,
                           mock_not_found_exception_class):
        exception = MagicMock()
        exception.code = 404
        mock_request.path.startswith.return_value = False
        mock_render_template.return_value = '404.html'

        result, status_code = error_handler(exception)
        self.assertEqual(result, '404.html', 'result should be 404.html')
        self.assertEqual(status_code, 404, 'status_code should be 404')
        mock_render_template.assert_called_once_with('404.html')

        mock_request.path.startswith.return_value = True
        mock_request.full_path = '/api/abcd'
        mock_api_exception_handler.return_value = 'exception'
        mock_not_found_exception_class.return_value = 'not-found-exception'

        result = error_handler(exception)
        self.assertEqual(result, 'exception', 'result should be "exception"')
        mock_not_found_exception_class.\
            assert_called_once_with('Not Found',
                                    description="'/api/abcd' path not found")
        mock_api_exception_handler.assert_called_once_with('not-found-exception')
