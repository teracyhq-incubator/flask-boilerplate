from mock import patch, MagicMock
from nose.plugins.attrib import attr

from tests.unit import UnitTestCase


class JsonTestCase(UnitTestCase):

    @attr('smoke')
    @patch('app.api.representations.json.current_app')
    @patch('app.api.representations.json.make_response')
    def test_output_json(self, mock_make_response, mock_current_app):
        settings = {}
        mock_current_app.config.get.return_value = settings
        mock_current_app.debug = False

        mock_output = MagicMock()

        mock_make_response.return_value = mock_output

        from app.api.representations.json import output_json

        data = {
            'hello': 'world'
        }
        code = 200
        headers = {
            'X-APPLICATION': 'Flask'
        }

        output = output_json(data, code, headers)

        self.assertEqual(settings, {})
        self.assertEqual(output, mock_output)

        mock_output.headers.__setitem__.called_once_with('Content-Type', 'application/json')
        mock_output.headers.extend.assert_called_once_with(headers)
        self.assertTrue(mock_make_response.call_count, 1)
        mock_current_app.config.get.assert_called_once_with('RESTFUL_JSON', {})

    @patch('app.api.representations.json.current_app')
    @patch('app.api.representations.json.make_response')
    def test_output_json_debug(self, mock_make_response, mock_current_app):
        settings = {}
        mock_current_app.config.get.return_value = settings
        mock_current_app.debug = True

        mock_output = MagicMock()

        mock_make_response.return_value = mock_output

        from app.api.representations.json import output_json

        data = {
            'hello': 'world'
        }
        code = 200
        headers = {
            'X-APPLICATION': 'Flask'
        }

        output = output_json(data, code, headers)

        self.assertEqual(settings.get('indent'), 4)
        self.assertEqual(settings.get('sort_keys'), True)

        self.assertEqual(output, mock_output)

        mock_output.headers.__setitem__.called_once_with('Content-Type', 'application/json')
        mock_output.headers.extend.assert_called_once_with(headers)
        self.assertTrue(mock_make_response.call_count, 1)
        mock_current_app.config.get.assert_called_once_with('RESTFUL_JSON', {})
