# -*- coding: utf-8 -*-

"""app.api.base tests"""
from mock import patch, MagicMock
from flask import make_response
from flask_restful import Resource

from tests.unit import UnitTestCase
from tests.unit.app import CurrentAppMockMixin


class BaseTestCase(CurrentAppMockMixin, UnitTestCase):
    @patch('app.api.base.marshal_with')
    def test_marshal_with_data_envelop(self, mock_marshal_with):
        from app.api.base import marshal_with_data_envelope

        marshal_with_data_envelope({'hi': 'there'})
        mock_marshal_with.assert_called_once_with({'hi': 'there'}, envelope='data')

    @patch('app.api.base.auth_datastore')
    def test_jwt_authenticate_none(self, mock_datastore):
        from app.api.base import jwt_authenticate

        mock_datastore.find_users.return_value.first.return_value = None
        user = jwt_authenticate('email', 'password')

        self.assertIsNone(user)
        mock_datastore.find_users.assert_called_once_with(email='email')

    @patch('app.api.base.utils')
    @patch('app.api.base.auth_datastore')
    def test_jwt_authenticate_not_verified(self, mock_datastore, mock_utils):
        from app.api.base import jwt_authenticate

        mock_datastore.find_users.return_value.first.return_value = 'user'
        mock_utils.verify_and_update_password.return_value = False

        user = jwt_authenticate('email', 'password')

        self.assertIsNone(user)
        mock_datastore.find_users.assert_called_once_with(email='email')
        mock_utils.verify_and_update_password.assert_called_once_with('password', 'user')

    @patch('app.api.base.utils')
    @patch('app.api.base.auth_datastore')
    def test_jwt_authenticate_verified(self, mock_datastore, mock_utils):
        from app.api.base import jwt_authenticate

        mock_datastore.find_users.return_value.first.return_value = 'found'
        mock_utils.verify_and_update_password.return_value = True

        user = jwt_authenticate('email', 'password')

        self.assertEqual(user, 'found')
        mock_datastore.find_users.assert_called_once_with(email='email')
        mock_utils.verify_and_update_password.assert_called_once_with('password', 'found')

    @patch('app.api.base.safe_str_cmp')
    @patch('app.api.base.auth_datastore')
    def test_jwt_load_user_anonymous(self, mock_datastore, mock_safe_str_cmp):
        from app.api.base import jwt_load_user, md5, AnonymousUser

        mock_datastore.read_user.return_value = None

        payload = {
            'sub': 1,
            'pwd': md5('password')
        }

        user = jwt_load_user(payload)

        self.assertTrue(isinstance(user, AnonymousUser))
        mock_datastore.read_user.assert_called_once_with(payload['sub'])
        mock_safe_str_cmp.assert_not_called()

    @patch('app.api.base.auth_datastore')
    def test_jwt_load_user_verified(self, mock_datastore):
        from app.api.base import jwt_load_user, md5
        from app.auth.models import User

        returned_user = User(password='password')
        mock_datastore.read_user.return_value = returned_user

        payload = {
            'sub': 1,
            'pwd': md5('password')
        }

        user = jwt_load_user(payload)

        self.assertEqual(user, returned_user)
        mock_datastore.read_user.assert_called_once_with(payload['sub'])

    def test_jwt_make_payload_default(self):
        from app.api.base import jwt_make_payload, md5, current_app, timedelta
        from app.auth.models import User

        user = User(id=1, password='pwd')

        payload = jwt_make_payload(user)

        self.assertEqual(payload['sub'], 1)
        self.assertEqual(payload['pwd'], md5('pwd'))
        self.assertIsNotNone(payload['iat'])
        expected_exp = payload['iat'] + current_app.config['JWT_EXPIRATION_DELTA'] + timedelta(
            seconds=current_app.config['JWT_LEEWAY'])
        self.assertEqual(payload['exp'], expected_exp)

    def test_jwt_make_payload_options(self):
        from app.api.base import jwt_make_payload, md5, timedelta
        from app.auth.models import User

        user = User(id=1, password='pwd')
        expiration_delta = timedelta(hours=3)
        leeway = 5

        payload = jwt_make_payload(user, expiration_delta, leeway)

        self.assertEqual(payload['sub'], 1)
        self.assertEqual(payload['pwd'], md5('pwd'))
        self.assertIsNotNone(payload['iat'])
        expected_exp = payload['iat'] + expiration_delta + timedelta(seconds=leeway)
        self.assertEqual(payload['exp'], expected_exp)

    @patch('app.api.base.jwt_lib')
    def test_jwt_encode_payload(self, mock_jwt_lib):
        from app.api.base import jwt_encode_payload, current_app

        payload = {
            'sub': 2
        }

        mock_jwt_lib.encode.return_value = 'encoded'

        encoded = jwt_encode_payload(payload)

        self.assertEqual(encoded, 'encoded')

        mock_jwt_lib.encode.assert_called_once_with(payload, current_app.config['JWT_SECRET_KEY'],
                                                    algorithm=current_app.config['JWT_ALGORITHM'])

    @patch('app.api.base.jwt_lib')
    def test_jwt_decode_token(self, mock_jwt_lib):
        from app.api.base import jwt_decode_token, current_app

        token = 'token'

        mock_jwt_lib.decode.return_value = 'payload'

        payload = jwt_decode_token(token)

        self.assertEqual(payload, 'payload')

        mock_jwt_lib.decode.assert_called_once_with(token, current_app.config['JWT_SECRET_KEY'],
                                                    algorithms=current_app.config['JWT_ALGORITHMS'])

    @patch('app.api.base.ApplicationException')
    @patch('app.api.base.api_exception_handler')
    def test_jwt_error(self, mock_api_exception_handler, mock_application_exception_class):
        from app.api.base import jwt_error
        from flask_jwt import JWTError

        ex = JWTError('error', 'error description')
        mock_api_exception_handler.return_value = 'response'

        result = jwt_error(ex)

        self.assertEqual(result, 'response')
        self.assertEqual(mock_api_exception_handler.call_count, 1)
        mock_application_exception_class.assert_called_once_with(ex.error,
                                                                 description=ex.description,
                                                                 status_code=ex.status_code)

    def test_make_empty_response(self):

        from functools import partial
        from app.api.base import make_empty_response

        self.assertEqual(type(make_empty_response), partial)
        self.assertEqual(make_empty_response.args, ('',))
        self.assertEqual(make_empty_response.func, make_response)

    def test_supported_ops(self):

        from app.api.base import SUPPORTED_OPS

        supported_ops = ['eq', 'ne', 'lt', 'le', 'gt', 'ge', 'lk', 'nl', 'in', 'ni', 'ct', 'mc']

        for op in supported_ops:
            self.assertTrue(op in SUPPORTED_OPS, '{} should be in SUPPORTED_OPS'.format(op))

    def test_filter_key_regex(self):

        from app.api.base import FILTER_KEY_REGEX

        check_list = [
            ('name', False),
            ('name_', False),
            ('name__', False),
            ('_name_', False),
            ('name__ab', False),
            ('name__eq', True),
            ('_name__ne', True),
            ('a__ne', True),
            ('ab__lt', True),
            ('abc__le', True),
            ('def__gt', True),
            ('ghi__ge', True),
            ('jkl__lk', True),
            ('lmdd__nl', True),
            ('_ahoige__in', True),
            ('__dhoaihgeoiage__ni', True),
            ('ahgoiedadf__ct', True),
            ('nameddd__mc', True),
        ]

        for key, valid in check_list:
            if valid:
                self.assertTrue(FILTER_KEY_REGEX.match(key),
                                '{} should match {}'.format(key, FILTER_KEY_REGEX.pattern))
            else:
                self.assertFalse(FILTER_KEY_REGEX.match(key),
                                 '{} should not match {}'.format(key, FILTER_KEY_REGEX.pattern))

    def test_sq_ops_mapper(self):
        from app.api.base import SA_OPS_MAPPER

        check_list = [
            ('eq', 'eq'),
            ('ne', 'ne'),
            ('lt', 'lt'),
            ('le', 'le'),
            ('gt', 'gt'),
            ('ge', 'ge'),
            ('lk', 'like'),
            ('nl', 'notlike'),
            ('in', 'in_'),
            ('ni', 'notin_'),
            ('ct', 'contains'),
            ('mc', 'match')
        ]

        for key, value in check_list:
            self.assertEqual(SA_OPS_MAPPER.get(key), value, '{} should match {}'.format(key, value))


class ResourceTestCase(CurrentAppMockMixin, UnitTestCase):
    def test_something(self):
        pass

class TokenRequiredResourceTestCase(CurrentAppMockMixin, UnitTestCase):
    def test_class(self):
        from app.api.base import TokenRequiredResource, Resource

        self.assertTrue(issubclass(TokenRequiredResource, Resource))

    def test_decorators(self):
        from app.api.base import TokenRequiredResource

        self.assertEqual(len(TokenRequiredResource.decorators), 1,
                         'len(AdminRoleRequiredResource.decorators) should be 1')
        # TODO(hoatle): add more asserts


class AdminRoleRequiredResourceTestCase(CurrentAppMockMixin, UnitTestCase):
    def test_class(self):
        from app.api.base import AdminRoleRequiredResource, Resource

        self.assertTrue(issubclass(AdminRoleRequiredResource, Resource))

    def test_decorators(self):
        from app.api.base import AdminRoleRequiredResource

        self.assertEqual(len(AdminRoleRequiredResource.decorators), 2,
                         'len(AdminRoleRequiredResource.decorators) should be 2')
        # TODO(hoatle): add more asserts
