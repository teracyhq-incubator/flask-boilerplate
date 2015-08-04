# -*- coding: utf-8 -*-

"""auth.decorators tests"""

from mock import Mock, patch
from werkzeug.exceptions import HTTPException
from flask_principal import PermissionDenied

from app.auth.permissions import user_permission, admin_role_permission
from app.auth.decorators import (permissions_accepted, permissions_required, roles_required,
                                 roles_accepted)
from tests.unit import UnitTestCase


class DecoratorsTestCase(UnitTestCase):

    def test_permissions_required(self):

        mock_user_permission = Mock(spec=user_permission)
        mock_admin_role_permission = Mock(spec=admin_role_permission)

        mock_user_permission.return_value.can.return_value = False
        mock_admin_role_permission.can.return_value = False

        @permissions_required(mock_user_permission, mock_admin_role_permission)
        def test(user_id):
            return 'permission_required: {}'.format(user_id)

        self.assertRaises(PermissionDenied, test, 1)

        mock_user_permission.return_value.can.return_value = True

        self.assertRaises(PermissionDenied, test, 2)

        mock_user_permission.return_value.can.return_value = False
        mock_admin_role_permission.can.return_value = True

        self.assertRaises(PermissionDenied, test, 3)

        mock_user_permission.return_value.can.return_value = True

        self.assertEqual(test(4), 'permission_required: 4',
                         'test(4) should return "permission_required: 4"')

    def test_permissions_required_http_exception(self):
        mock_user_permission = Mock(spec=user_permission)
        mock_admin_role_permission = Mock(spec=admin_role_permission)

        mock_user_permission.return_value.can.return_value = False
        mock_admin_role_permission.can.return_value = False

        @permissions_required(mock_user_permission, mock_admin_role_permission, http_exception=403)
        def test(user_id):
            return 'permission_required: {}'.format(user_id)

        self.assertRaises(HTTPException, test, 1)

        mock_user_permission.return_value.can.return_value = True

        self.assertRaises(HTTPException, test, 2)

        mock_user_permission.return_value.can.return_value = False
        mock_admin_role_permission.can.return_value = True

        self.assertRaises(HTTPException, test, 3)

        mock_user_permission.return_value.can.return_value = True

        self.assertEqual(test(4), 'permission_required: 4',
                         'test(4) should return "permission_required: 4"')

    def test_permissions_required_exception_handler(self):
        mock_user_permission = Mock(spec=user_permission)
        mock_admin_role_permission = Mock(spec=admin_role_permission)

        mock_user_permission.return_value.can.return_value = False
        mock_admin_role_permission.can.return_value = False

        class MyException(Exception):
            pass

        def exception_handler(permission):
            raise MyException

        @permissions_required(mock_user_permission, mock_admin_role_permission,
                              exception_handler=exception_handler)
        def test(user_id):
            return 'permission_required: {}'.format(user_id)

        self.assertRaises(MyException, test, 1)

        mock_user_permission.return_value.can.return_value = True

        self.assertRaises(MyException, test, 2)

        mock_user_permission.return_value.can.return_value = False
        mock_admin_role_permission.can.return_value = True

        self.assertRaises(MyException, test, 3)

        mock_user_permission.return_value.can.return_value = True

        self.assertEqual(test(4), 'permission_required: 4',
                         'test(4) should return "permission_required: 4"')

    def test_permissions_accepted(self):
        mock_user_permission = Mock(spec=user_permission)
        mock_admin_role_permission = Mock(spec=admin_role_permission)

        mock_user_permission.return_value.can.return_value = False
        mock_admin_role_permission.can.return_value = False

        @permissions_accepted(mock_user_permission, mock_admin_role_permission)
        def test(user_id):
            return 'permission_accepted: {}'.format(user_id)

        self.assertRaises(PermissionDenied, test, 1)

        mock_user_permission.return_value.can.return_value = True

        self.assertEqual(test(2), 'permission_accepted: 2',
                         'test(2) should return "permission_accepted: 2"')

        mock_user_permission.return_value.can.return_value = False
        mock_admin_role_permission.can.return_value = True

        self.assertEqual(test(3), 'permission_accepted: 3',
                         'test(3) should return "permission_accepted: 3"')

        mock_user_permission.return_value.can.return_value = True

        self.assertEqual(test(4), 'permission_accepted: 4',
                         'test(4) should return "permission_accepted: 4"')

    def test_permissions_accepted_http_exception(self):
        mock_user_permission = Mock(spec=user_permission)
        mock_admin_role_permission = Mock(spec=admin_role_permission)

        mock_user_permission.return_value.can.return_value = False
        mock_admin_role_permission.can.return_value = False

        @permissions_accepted(mock_user_permission, mock_admin_role_permission, http_exception=403)
        def test(user_id):
            return 'permission_accepted: {}'.format(user_id)

        self.assertRaises(HTTPException, test, 1)

        mock_user_permission.return_value.can.return_value = True

        self.assertEqual(test(2), 'permission_accepted: 2',
                         'test(2) should return "permission_accepted: 2"')

        mock_user_permission.return_value.can.return_value = False
        mock_admin_role_permission.can.return_value = True

        self.assertEqual(test(3), 'permission_accepted: 3',
                         'test(3) should return "permission_accepted: 3"')

        mock_user_permission.return_value.can.return_value = True

        self.assertEqual(test(4), 'permission_accepted: 4',
                         'test(4) should return "permission_accepted: 4"')

    def test_permissions_accepted_exception_handler(self):
        mock_user_permission = Mock(spec=user_permission)
        mock_admin_role_permission = Mock(spec=admin_role_permission)

        mock_user_permission.return_value.can.return_value = False
        mock_admin_role_permission.can.return_value = False

        class MyException(Exception):
            pass

        def exception_handler(permissions):
            raise MyException

        @permissions_accepted(mock_user_permission, mock_admin_role_permission,
                              exception_handler=exception_handler)
        def test(user_id):
            return 'permission_accepted: {}'.format(user_id)

        self.assertRaises(MyException, test, 1)

        mock_user_permission.return_value.can.return_value = True

        self.assertEqual(test(2), 'permission_accepted: 2',
                         'test(2) should return "permission_accepted: 2"')

        mock_user_permission.return_value.can.return_value = False
        mock_admin_role_permission.can.return_value = True

        self.assertEqual(test(3), 'permission_accepted: 3',
                         'test(3) should return "permission_accepted: 3"')

        mock_user_permission.return_value.can.return_value = True

        self.assertEqual(test(4), 'permission_accepted: 4',
                         'test(4) should return "permission_accepted: 4"')

    @patch('app.auth.decorators.Permission')
    def test_roles_required(self, mock_permission):
        true_true_return_values = [True, True]
        true_false_return_values = [True, False]
        false_true_return_values = [False, True]
        false_false_return_values = [False, False]

        @roles_required('admin', 'editor')
        def test(user_id):
            return 'roles_required: {}'.format(user_id)

        mock_permission.return_value.can.side_effect = lambda: true_true_return_values.pop()
        self.assertEqual(test(1), 'roles_required: 1', "test(1) should return 'roles_required: 1'")

        mock_permission.return_value.can.side_effect = lambda: true_false_return_values.pop()
        self.assertRaises(PermissionDenied, test, 2)

        mock_permission.return_value.can.side_effect = lambda: false_true_return_values.pop()
        self.assertRaises(PermissionDenied, test, 3)

        mock_permission.return_value.can.side_effect = lambda: false_false_return_values.pop()
        self.assertRaises(PermissionDenied, test, 4)

    @patch('app.auth.decorators.Permission')
    def test_roles_required_http_exception(self, mock_permission):
        true_true_return_values = [True, True]
        true_false_return_values = [True, False]
        false_true_return_values = [False, True]
        false_false_return_values = [False, False]

        @roles_required('admin', 'editor', http_exception=403)
        def test(user_id):
            return 'roles_required: {}'.format(user_id)

        mock_permission.return_value.can.side_effect = lambda: true_true_return_values.pop()
        self.assertEqual(test(1), 'roles_required: 1', "test(1) should return 'roles_required: 1'")

        mock_permission.return_value.can.side_effect = lambda: true_false_return_values.pop()
        self.assertRaises(HTTPException, test, 2)

        mock_permission.return_value.can.side_effect = lambda: false_true_return_values.pop()
        self.assertRaises(HTTPException, test, 3)

        mock_permission.return_value.can.side_effect = lambda: false_false_return_values.pop()
        self.assertRaises(HTTPException, test, 4)

    @patch('app.auth.decorators.Permission')
    def test_roles_required_exception_handler(self, mock_permission):
        true_true_return_values = [True, True]
        true_false_return_values = [True, False]
        false_true_return_values = [False, True]
        false_false_return_values = [False, False]

        class MyException(Exception):
            pass

        def my_exception_handler(permission):
            raise MyException(permission)

        @roles_required('admin', 'editor', exception_handler=my_exception_handler)
        def test(user_id):
            return 'roles_required: {}'.format(user_id)

        mock_permission.return_value.can.side_effect = lambda: true_true_return_values.pop()
        self.assertEqual(test(1), 'roles_required: 1', "test(1) should return 'roles_required: 1'")

        mock_permission.return_value.can.side_effect = lambda: true_false_return_values.pop()
        self.assertRaises(MyException, test, 2)

        mock_permission.return_value.can.side_effect = lambda: false_true_return_values.pop()
        self.assertRaises(MyException, test, 3)

        mock_permission.return_value.can.side_effect = lambda: false_false_return_values.pop()
        self.assertRaises(MyException, test, 4)

    @patch('app.auth.decorators.Permission')
    def test_roles_accepted(self, mock_permission):
        true_true_return_values = [True, True]
        true_false_return_values = [True, False]
        false_true_return_values = [False, True]
        false_false_return_values = [False, False]

        @roles_accepted('admin', 'editor')
        def test(user_id):
            return 'roles_accepted: {}'.format(user_id)

        mock_permission.return_value.can.side_effect = lambda: true_true_return_values.pop()
        self.assertEqual(test(1), 'roles_accepted: 1', "test(1) should return 'roles_accepted: 1'")

        mock_permission.return_value.can.side_effect = lambda: true_false_return_values.pop()
        self.assertEqual(test(2), 'roles_accepted: 2', "test(2) should return 'roles_accepted: 2'")

        mock_permission.return_value.can.side_effect = lambda: false_true_return_values.pop()
        self.assertEqual(test(3), 'roles_accepted: 3', "test(1) should return 'roles_accepted: 3'")

        mock_permission.return_value.can.side_effect = lambda: false_false_return_values.pop()
        self.assertRaises(PermissionDenied, test, 4)

    @patch('app.auth.decorators.Permission')
    def test_roles_accepted_http_exception(self, mock_permission):
        true_true_return_values = [True, True]
        true_false_return_values = [True, False]
        false_true_return_values = [False, True]
        false_false_return_values = [False, False]

        @roles_accepted('admin', 'editor', http_exception=403)
        def test(user_id):
            return 'roles_accepted: {}'.format(user_id)

        mock_permission.return_value.can.side_effect = lambda: true_true_return_values.pop()
        self.assertEqual(test(1), 'roles_accepted: 1', "test(1) should return 'roles_accepted: 1'")

        mock_permission.return_value.can.side_effect = lambda: true_false_return_values.pop()
        self.assertEqual(test(2), 'roles_accepted: 2', "test(2) should return 'roles_accepted: 2'")

        mock_permission.return_value.can.side_effect = lambda: false_true_return_values.pop()
        self.assertEqual(test(3), 'roles_accepted: 3', "test(1) should return 'roles_accepted: 3'")

        mock_permission.return_value.can.side_effect = lambda: false_false_return_values.pop()
        self.assertRaises(HTTPException, test, 4)

    @patch('app.auth.decorators.Permission')
    def test_roles_accepted_exception_handler(self, mock_permission):
        true_true_return_values = [True, True]
        true_false_return_values = [True, False]
        false_true_return_values = [False, True]
        false_false_return_values = [False, False]

        class MyException(Exception):
            pass

        def my_exception_handler(permissions):
            raise MyException(permissions)

        @roles_accepted('admin', 'editor', exception_handler=my_exception_handler)
        def test(user_id):
            return 'roles_accepted: {}'.format(user_id)

        mock_permission.return_value.can.side_effect = lambda: true_true_return_values.pop()
        self.assertEqual(test(1), 'roles_accepted: 1', "test(1) should return 'roles_accepted: 1'")

        mock_permission.return_value.can.side_effect = lambda: true_false_return_values.pop()
        self.assertEqual(test(2), 'roles_accepted: 2', "test(2) should return 'roles_accepted: 2'")

        mock_permission.return_value.can.side_effect = lambda: false_true_return_values.pop()
        self.assertEqual(test(3), 'roles_accepted: 3', "test(1) should return 'roles_accepted: 3'")

        mock_permission.return_value.can.side_effect = lambda: false_false_return_values.pop()
        self.assertRaises(MyException, test, 4)
