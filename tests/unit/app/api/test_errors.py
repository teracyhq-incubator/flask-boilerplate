# -*- coding: utf-8 -*-

"""tests for app.api.errors"""

from mock import patch, MagicMock


from tests.unit import UnitTestCase


class ErrorsTestCase(UnitTestCase):
    @patch('app.api.errors.request')
    @patch('app.api.errors.jsonify', lambda x: x)
    def test_api_exception_handler(self, mock_request):

        from app.api.errors import api_exception_handler

        exception = MagicMock()
        exception.to_json.return_value = '{"message": "something wrong happened"}'
        exception.status_code = 401

        json, status_code = api_exception_handler(exception)
        self.assertEqual(json, exception.to_json.return_value,
                         'json should be {}'.format(exception.to_json.return_value))
        self.assertEqual(status_code, 401,
                         'status_code should be 401')
        exception.to_json.assert_called_once_with()

        exception.reset_mock()

        mock_request.args = {
            'suppress_response_codes': 'true'
        }

        result = api_exception_handler(exception)
        self.assertEqual(result, exception.to_json.return_value,
                         'result should be {}'.format(exception.to_json.return_value))
        exception.to_json.assert_called_once_with()

        exception.reset_mock()

        mock_request.args = {
            'suppress_response_codes': '1'
        }

        result = api_exception_handler(exception)
        self.assertEqual(result, exception.to_json.return_value,
                         'result should be {}'.format(exception.to_json.return_value))
        exception.to_json.assert_called_once_with()

        exception.reset_mock()
        mock_request.args = {
            'suppress_response_codes': '0'
        }
        exception.status_code = 403

        json, status_code = api_exception_handler(exception)
        self.assertEqual(json, exception.to_json.return_value,
                         'json should be {}'.format(exception.to_json.return_value))
        self.assertEqual(status_code, 403,
                         'status_code should be 403')
        exception.to_json.assert_called_once_with()
