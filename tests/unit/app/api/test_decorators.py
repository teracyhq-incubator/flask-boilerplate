# -*- coding: utf-8 -*-

"""tests for app.api.decorators"""
import collections
from mock import Mock, MagicMock, patch, call

from tests.unit import UnitTestCase
from app.api import (anonymous_required, token_auth_required, http_auth_required,
                     session_auth_required, auth_required, roles_required, roles_accepted, one_of,
                     permissions_required, permissions_accepted)

from app.exceptions import BadRequestException, UnauthorizedException


class DecoratorsTestCase(UnitTestCase):

    @patch('app.api.decorators.authenticated')
    def test_anonymous_required(self, mock_authenticated):
        mock_authenticated.return_value = False

        @anonymous_required
        def test():
            return 'anonymous_required'

        self.assertEqual(test(), 'anonymous_required',
                         'test() should return {}'.format('anonymous_required'))

        mock_authenticated.return_value = True
        self.assertRaises(BadRequestException, test)

    @patch('app.api.decorators.current_user')
    @patch('app.api.decorators.verify_jwt')
    def test_token_auth_required_unauthorized(self, mock_verify_jwt, mock_current_user):

        mock_current_user.is_authenticated.return_value = False

        @token_auth_required('realm')
        def test():
            return 'token_auth_required'

        with self.assertRaises(UnauthorizedException) as uae:
            test()
        ex = uae.exception
        self.assertIsInstance(ex, UnauthorizedException)
        self.assertTrue(ex.message, 'Invalid Token')
        mock_verify_jwt.assert_called_once_with('realm')
        mock_current_user.is_authenticated.assert_called_once_with()

    @patch('app.api.decorators.identity_changed')
    @patch('app.api.decorators._request_ctx_stack')
    @patch('app.api.decorators.current_app')
    @patch('app.api.decorators.current_user')
    @patch('app.api.decorators.verify_jwt')
    def test_token_auth_required_authorized(self, mock_verify_jwt, mock_current_user,
                                            mock_current_app, mock_request_ctx_stack,
                                            mock_identity_changed):

        mock_current_user.is_authenticated.return_value = True

        @token_auth_required('realm')
        def test():
            return 'token_auth_required'

        self.assertEqual(test(), 'token_auth_required',
                         'test() should return {}'.format('token_auth_required'))

        mock_verify_jwt.assert_called_once_with('realm')
        mock_current_user.is_authenticated.assert_called_once_with()
        mock_current_app._get_current_object.assert_called_once_with()
        self.assertEqual(mock_request_ctx_stack.top.user, mock_current_user)
        self.assertEqual(mock_identity_changed.send.call_count, 1)

    @patch('app.api.decorators.http_authenticated')
    def test_http_auth_required(self, mock_http_authenticated):
        mock_http_authenticated.return_value = True

        @http_auth_required
        def test():
            return 'http_auth_required'

        self.assertEqual(test(), 'http_auth_required',
                         'test() should return {}'.format('http_auth_required'))

        mock_http_authenticated.return_value = False
        self.assertRaises(UnauthorizedException, test)

    @patch('app.api.decorators.session_authenticated')
    def test_session_auth_required(self, mock_session_authenticated):
        mock_session_authenticated.return_value = True

        @session_auth_required
        def test():
            return 'session_auth_required'

        self.assertEqual(test(), 'session_auth_required',
                         'test() should return {}'.format(session_auth_required))

        mock_session_authenticated.return_value = False
        self.assertRaises(UnauthorizedException, test)

    @patch('app.api.decorators.token_authenticated')
    @patch('app.api.decorators.http_authenticated')
    @patch('app.api.decorators.session_authenticated')
    def test_auth_required(self, mock_token_authenticated, mock_http_authenticated,
                           mock_session_authenticated):

        mock_token_authenticated.return_value = False
        mock_http_authenticated.return_value = False
        mock_session_authenticated.return_value = False

        @auth_required('token', 'basic', 'session')
        def test():
            return 'authenticated'

        self.assertRaises(UnauthorizedException, test)

        mock_token_authenticated.return_value = True

        self.assertEqual(test(), 'authenticated', 'test() should return {}'.format('authenticated'))

        mock_token_authenticated.return_value = False
        mock_http_authenticated.return_value = True
        self.assertEqual(test(), 'authenticated', 'test() should return {}'.format('authenticated'))

        mock_http_authenticated.return_value = False
        mock_session_authenticated.return_value = True
        self.assertEqual(test(), 'authenticated', 'test() should return {}'.format('authenticated'))

    @patch('app.api.decorators.auth_permissions_required')
    def test_permissions_required(self, mock_permissions_required):
        permissions = [Mock(), Mock()]

        permissions_required(*permissions)

        self.assertEqual(mock_permissions_required.call_count, 1)
        # see: http://stackoverflow.com/questions/9623114/check-if-two-unordered-lists-are-equal
        self.assertEqual(collections.Counter(mock_permissions_required.call_args[0]),
                         collections.Counter(permissions))
        exception_handler = mock_permissions_required.call_args[1].get('exception_handler')
        self.assertTrue(callable(exception_handler))
        self.assertRaises(UnauthorizedException, exception_handler, permissions[1])

    @patch('app.api.decorators.auth_permissions_accepted')
    def test_permissions_accepted(self, mock_auth_permission_accepted):
        permissions = [Mock(), Mock()]

        permissions_accepted(*permissions)

        self.assertEqual(mock_auth_permission_accepted.call_count, 1)
        self.assertEqual(len(mock_auth_permission_accepted.call_args), 2)
        # see: http://stackoverflow.com/questions/9623114/check-if-two-unordered-lists-are-equal
        self.assertEqual(collections.Counter(mock_auth_permission_accepted.call_args[0]),
                         collections.Counter(permissions))
        exception_handler = mock_auth_permission_accepted.call_args[1].get('exception_handler')
        self.assertTrue(callable(exception_handler))
        self.assertRaises(UnauthorizedException, exception_handler, permissions)

    @patch('app.api.decorators.auth_roles_required')
    def test_roles_required(self, mock_roles_required):
        roles = ['admin', 'editor']
        roles_required(*roles)

        self.assertEqual(mock_roles_required.call_count, 1)
        self.assertEqual(len(mock_roles_required.call_args), 2)
        # see: http://stackoverflow.com/questions/9623114/check-if-two-unordered-lists-are-equal
        self.assertEqual(collections.Counter(mock_roles_required.call_args[0]),
                         collections.Counter(roles))
        exception_handler = mock_roles_required.call_args[1].get('exception_handler')
        self.assertTrue(callable(exception_handler))
        self.assertRaises(UnauthorizedException, exception_handler, roles)

    @patch('app.api.decorators.auth_roles_accepted')
    def test_roles_accepted(self, mock_roles_accepted):
        roles = ['admin', 'editor']
        roles_accepted(*roles)

        self.assertEqual(mock_roles_accepted.call_count, 1)
        self.assertEqual(len(mock_roles_accepted.call_args), 2)
        # see: http://stackoverflow.com/questions/9623114/check-if-two-unordered-lists-are-equal
        self.assertEqual(collections.Counter(mock_roles_accepted.call_args[0]),
                         collections.Counter(roles))
        exception_handler = mock_roles_accepted.call_args[1].get('exception_handler')
        self.assertTrue(callable(exception_handler))
        self.assertRaises(UnauthorizedException, exception_handler, roles)

    def test_one_of(self):

        from app.exceptions import ApplicationException

        def result():
            return 'one_of'

        mock_decorator_1 = Mock(return_value=result)
        mock_decorator_2 = Mock(return_value=result)
        mock_decorator_3 = Mock(side_effect=Exception('exception'))
        mock_decorator_4 = Mock(
            side_effect=ApplicationException('app exception', description='description exception'))

        @one_of(mock_decorator_1, mock_decorator_2)
        def test1():
            return result

        self.assertEqual(test1(), 'one_of', 'test1() should return {}'.format('one_of'))

        @one_of(mock_decorator_3, mock_decorator_2)
        def test2():
            return result

        self.assertEqual(test2(), 'one_of', 'test2() should return {}'.format('one_of'))

        @one_of(mock_decorator_3, mock_decorator_4)
        def test3():
            return result

        with self.assertRaises(ApplicationException) as ex:
            test3()
        ex_3 = ex.exception
        self.assertIsInstance(ex_3, ApplicationException)
        self.assertEqual(ex_3.message, 'app exception or exception')
        self.assertEqual(ex_3.description, 'description exception')

        mock_decorator_3.side_effect = Exception('exception')
        mock_decorator_4.side_effect = ApplicationException('app exception',
                                                            description='description exception')

        @one_of(mock_decorator_4, mock_decorator_3)
        def test_4():
            return result

        with self.assertRaises(ApplicationException) as ex:
            test_4()

        ex_4 = ex.exception
        self.assertIsInstance(ex_4, ApplicationException)
        self.assertEqual(ex_4.message, 'exception or app exception')
        self.assertEqual(ex_4.description, 'description exception')

        @one_of()
        def test5():
            return result()
        self.assertEqual(test5(), 'one_of', 'test5() should return {}'.format('one_of'))

    @patch('app.api.decorators.OffsetPagination')
    def test_paginated_one(self, mock_offset_pagination):

        from app.api.decorators import paginated

        mock_query = MagicMock()
        mock_args = MagicMock()

        mock_query.one.return_value = '1'

        mock_args.get.side_effect = [
            True
        ]

        @paginated
        def test():
            return mock_query, mock_args

        result = test()

        expected_result = {
            'data': ['1'],
            'paging': {
                'count': 1,
                'offset': 0,
                'limit': 1,
                'previous': None,
                'next': None
            }
        }

        self.assertEqual(result, expected_result)
        mock_args.get.assert_called_once_with('one', False)
        mock_query.one.assert_called_once_with()
        self.assertFalse(mock_offset_pagination.called)

    @patch('app.api.decorators.OffsetPagination')
    def test_paginated_many(self, mock_offset_pagination):

        from app.api.decorators import paginated

        pagination = MagicMock()
        mock_offset_pagination.return_value = pagination

        pagination.data = ['hi', 'there']
        pagination.count = 7
        pagination.offset = 0
        pagination.limit = 2
        pagination.prev_url = None
        pagination.next_url = 'next_url'

        mock_query = MagicMock()
        mock_args = MagicMock()

        mock_args.get.side_effect = [
            None,
            0,
            2
        ]

        @paginated
        def test():
            return mock_query, mock_args

        result = test()

        expected_result = {
            'data': ['hi', 'there'],
            'paging': {
                'count': 7,
                'offset': 0,
                'limit': 2,
                'previous': None,
                'next': 'next_url'
            }
        }

        mock_offset_pagination.assert_called_once_with(mock_query, offset=0, limit=2)
        mock_args.get.assert_has_calls([call('one', False),
                                        call('offset', None),
                                        call('limit', None)])
        self.assertEqual(result, expected_result)
