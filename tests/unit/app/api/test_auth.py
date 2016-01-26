# -*- coding: utf-8 -*-

"""tests for app.api.auth"""
from mock import patch, call

from tests.unit import UnitTestCase
from app.api.auth import (token_authenticated, http_authenticated, session_authenticated,
                          authenticated)


class AuthTestCase(UnitTestCase):

    @patch('app.api.auth._jwt_required')
    def test_verify_token_auth(self, mock_jwt_required):

        from app.api.auth import verify_token_auth
        from app.api.auth import JWTError

        mock_jwt_required.side_effect = JWTError('error', 'description')

        self.assertFalse(verify_token_auth(), 'verify_token_auth() should be False')
        mock_jwt_required.assert_called_once_with(None)

        mock_jwt_required.reset_mock()
        mock_jwt_required.side_effect = None

        self.assertTrue(verify_token_auth('test'), 'verify_token_auth() should be True')
        mock_jwt_required.assert_called_once_with('test')

    @patch('app.api.auth._check_http_auth')
    def test_verify_http_auth(self, mock_check_http_auth):
        from app.api.auth import verify_http_auth

        mock_check_http_auth.return_value = True

        self.assertTrue(verify_http_auth(), 'verify_http_auth() should be True')
        mock_check_http_auth.assert_called_once_with()

        mock_check_http_auth.reset_mock()
        mock_check_http_auth.return_value = False

        self.assertFalse(verify_http_auth(), 'verify_http_auth() should be False')
        mock_check_http_auth.assert_called_once_with()

    @patch('app.api.auth.verify_token_auth')
    @patch('app.api.auth.g')
    def test_token_authenticated(self, mock_g, mock_verify_token_auth):
        mock_verify_token_auth.return_value = True
        self.assertTrue(token_authenticated(), 'token_authenticated() should be True')
        self.assertTrue(mock_g.token_auth_used)

        mock_verify_token_auth.return_value = False
        self.assertFalse(token_authenticated(), 'token_authenticated() should be False')
        self.assertFalse(mock_g.token_auth_used)

    @patch('app.api.auth.verify_http_auth')
    @patch('app.api.auth.g')
    def test_http_authenticated(self, mock_g, mock_verify_http_auth):
        mock_verify_http_auth.return_value = True
        self.assertTrue(http_authenticated(), 'http_authenticated() should be True')
        self.assertTrue(mock_g.http_auth_used)

        mock_verify_http_auth.return_value = False
        self.assertFalse(http_authenticated(), 'http_authenticated() should be False')
        self.assertFalse(mock_g.http_auth_used)

    @patch('app.api.auth.current_user')
    @patch('app.api.auth.g')
    def test_session_authenticated(self, mock_g, mock_current_user):
        mock_g.token_auth_used = False
        mock_g.http_auth_used = False
        mock_current_user.is_authenticated.return_value = True
        self.assertTrue(session_authenticated(), 'session_authenticated() should be True')

        mock_g.token_auth_used = True
        self.assertFalse(session_authenticated(), 'session_authenticated() should be False')

        mock_g.http_auth_used = True
        self.assertFalse(session_authenticated(), 'session_authenticated() should be False')

        mock_g.token_auth_used = False
        mock_g.http_auth_used = False
        mock_current_user.is_authenticated.return_value = False
        self.assertFalse(session_authenticated(), 'session_authenticated() should be False')

    @patch('app.api.auth.current_user')
    @patch('app.api.auth.g')
    def test_authenticated(self, mock_g, mock_current_user):
        mock_g.token_auth_used = False
        mock_g.http_auth_used = False
        mock_current_user.is_authenticated.return_value = False

        self.assertFalse(authenticated(), 'authenticated() should be False')

        mock_current_user.is_authenticated.return_value = True

        self.assertTrue(authenticated(), 'authenticated() should be True')

        mock_current_user.is_authenticated.return_value = False
        mock_g.http_auth_used = True

        self.assertTrue(authenticated(), 'authenticated() should be True')

        mock_g.http_auth_used = False
        mock_g.token_auth_used = True

        self.assertTrue(authenticated(), 'authenticated() should be True')

        mock_g.http_auth_used = True
        mock_current_user.is_authenticated.return_value = True

        self.assertTrue(authenticated(), 'authenticated() should be True')
