# -*- coding: utf-8 -*-

"""tests for api_1_0.auth"""
from datetime import datetime, timedelta

from mock import patch, MagicMock

from app.exceptions import BadRequestException
from tests.unit import UnitTestCase
from tests.unit.app import CurrentAppMockMixin


class AuthTestCase(UnitTestCase):

    @patch('app.api_1_0.auth.g')
    def test_before_request(self, mock_g):
        from app.api_1_0.auth import before_request

        before_request()

        self.assertIsNone(mock_g.token_auth_used)
        self.assertIsNone(mock_g.http_auth_used)


class TokenAPITestCase(CurrentAppMockMixin, UnitTestCase):

    def test_action_decorators(self):
        from app.api_1_0.auth import TokenAPI

        self.assertIsNotNone(TokenAPI.action_decorators.get('get'))
        self.assertIsNone(TokenAPI.action_decorators.get('post'))

    @patch('app.api_1_0.auth.jwt_encode_payload')
    @patch('app.api_1_0.auth.jwt_make_payload')
    @patch('app.api_1_0.auth.current_user')
    def test_get(self, mock_current_user, mock_jwt_make_payload, mock_jwt_encode_payload):

        from app.api_1_0.auth import TokenAPI

        utc_now = datetime.utcnow()
        delta = timedelta(hours=4)
        payload = {
            'iat': utc_now,
            'exp': utc_now + delta
        }

        mock_jwt_make_payload.return_value = payload

        mock_jwt_encode_payload.return_value = '123456789'

        token_api = TokenAPI()
        mock_parse_arguments = MagicMock()
        mock_parse_arguments.get.return_value = None
        token_api.parse_arguments = lambda: mock_parse_arguments
        result = token_api.get()

        self.assertEqual(result.get('token'), '123456789',
                         "result.get('token') should return {}".format(123456789))
        self.assertEqual(result.get('expires_in'), delta.total_seconds())
        mock_jwt_make_payload.assert_called_once_with(mock_current_user, expiration_delta=None)
        mock_jwt_encode_payload.assert_called_once_with(payload)

    @patch('app.api_1_0.auth.jwt_authenticate')
    def test_post_not_authenticated(self, mock_jwt_authenticate):

        from app.api_1_0.auth import TokenAPI

        token_api = TokenAPI()
        args = {
            'email': 'test@example.com',
            'password': 'pass',
            'expires_in': None
        }

        token_api.parse_arguments = lambda: args
        mock_jwt_authenticate.return_value = None

        with self.assertRaises(BadRequestException) as bre:
            token_api.post()

        ex = bre.exception

        self.assertIsInstance(ex, BadRequestException)
        self.assertEqual(ex.message, 'Invalid Credentials')
        self.assertEqual(ex.description, 'email or password is not correct')

        mock_jwt_authenticate.assert_called_once_with(args.get('email'), args.get('password'))

    @patch('app.api_1_0.auth.jwt_encode_payload')
    @patch('app.api_1_0.auth.jwt_make_payload')
    @patch('app.api_1_0.auth.jwt_authenticate')
    def test_post_authenticated(self, mock_jwt_authenticate, mock_jwt_make_payload,
                                mock_jwt_encode_payload):
        from app.api_1_0.auth import TokenAPI

        utc_now = datetime.utcnow()
        delta = timedelta(hours=4)
        payload = {
            'iat': utc_now,
            'exp': utc_now + delta
        }

        mock_jwt_make_payload.return_value = payload

        mock_jwt_encode_payload.return_value = '123456789'

        token_api = TokenAPI()
        args = {
            'email': 'test@example.com',
            'password': 'pass',
            'expires_in': None
        }

        token_api.parse_arguments = lambda: args
        mock_user = MagicMock()
        mock_jwt_authenticate.return_value = mock_user

        result = token_api.post()

        self.assertEqual(result.get('token'), '123456789')
        self.assertEqual(result.get('expires_in'), delta.total_seconds())
        mock_jwt_authenticate.assert_called_once_with(args.get('email'), args.get('password'))
        mock_jwt_make_payload.assert_called_once_with(mock_user, expiration_delta=None)
        mock_jwt_encode_payload.assert_called_once_with(payload)
