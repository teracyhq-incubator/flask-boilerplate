# -*- coding: utf-8 -*-

"""base api"""

from functools import partial
import re
from datetime import datetime, timedelta

from flask import current_app, request, make_response
from flask_security import utils, AnonymousUser
from flask_security.utils import md5
from flask_restful import Resource, marshal_with
from flask_restful.inputs import boolean
from flask_restful.reqparse import RequestParser
from werkzeug.security import safe_str_cmp
import jwt as jwt_lib

from ..extensions import jwt, auth_datastore
from ..utils import extract_dict
from ..exceptions import ApplicationException
from . import roles_required, token_auth_required
from .validators import NumberRange
from .errors import api_exception_handler


def _add_if_not_none(adding_dict, key, val):
    """add existing key, val to a dict if the val is not None"""
    if val is not None:
        adding_dict[key] = val


def marshal_with_data_envelope(fields):
    """marshal with `data` envelope"""
    return marshal_with(fields, envelope='data')


@jwt.authentication_handler
def jwt_authenticate(email, pwd):
    """Register jwt authentication handler

    :param email: the provided email
    :param pwd: the provided password

    :return None or the matching user
    """
    user = auth_datastore.find_users(email=email).first()
    if user and utils.verify_and_update_password(pwd, user):
        return user


@jwt.user_handler
def jwt_load_user(payload):
    """Register jwt user handler

    :param payload:
    """
    user = auth_datastore.read_user(payload['sub'])
    if user and safe_str_cmp(md5(user.password), payload['pwd']):
        return user
    return AnonymousUser()


@jwt.payload_handler
def jwt_make_payload(user, expiration_delta=None, leeway=None):
    """Register jwt payload handler

    :param user:
    """
    if expiration_delta:
        # timedelta config supported only
        max_expiration_delta = current_app.config['JWT_MAX_EXPIRATION_DELTA']
        expiration_delta = expiration_delta if expiration_delta <= max_expiration_delta \
            else max_expiration_delta
    else:
        # timedelta config supported only
        expiration_delta = current_app.config['JWT_EXPIRATION_DELTA']

    leeway = timedelta(seconds=leeway) if leeway else timedelta(
        seconds=current_app.config['JWT_LEEWAY'])  # int config as seconds

    utc_now = datetime.utcnow()
    return {
        'sub': user.id,
        'pwd': md5(user.password),
        'iat': utc_now,
        'exp': utc_now + expiration_delta + leeway
    }


@jwt.encode_handler
def jwt_encode_payload(payload):
    """Register jwt encode handler

    :param payload:
    """
    return jwt_lib.encode(payload, current_app.config['JWT_SECRET_KEY'],
                          algorithm=current_app.config['JWT_ALGORITHM'])


@jwt.decode_handler
def jwt_decode_token(token):
    """Register jwt decode handler

    :param token:
    """
    return jwt_lib.decode(token, current_app.config['JWT_SECRET_KEY'],
                          algorithms=current_app.config['JWT_ALGORITHMS'])


@jwt.error_handler
def jwt_error(ex):
    """Register jwt error handler

    :param ex:
    :return:
    """
    ex = ApplicationException(ex.error, description=ex.description, status_code=ex.status_code)
    return api_exception_handler(ex)


# short cut of flask.make_response for making empty response
#: make_empty_response()
#: make_empty_response(201)
#: make_empty_response(201, {'header-key': 'value'})
make_empty_response = partial(make_response, '')

SUPPORTED_OPS = frozenset(['eq', 'ne', 'lt', 'le', 'gt', 'ge', 'lk', 'nl', 'in', 'ni', 'ct', 'mc'])

# sql alchemy ops mapper
SA_OPS_MAPPER = {
    'eq': 'eq',
    'ne': 'ne',
    'lt': 'lt',
    'le': 'le',
    'gt': 'gt',
    'ge': 'ge',
    'lk': 'like',
    'nl': 'notlike',
    'in': 'in_',
    'ni': 'notin_',
    'ct': 'contains',
    'mc': 'match'
}

FILTER_KEY_REGEX = re.compile(r'^(?P<key>\w*[a-zA-Z0-9])+__(?P<op>%s)$' % '|'.join(SUPPORTED_OPS))


class RequestParserResourceMixin(object):
    """The mixin for request parser handling
    """

    def __init__(self):
        self.req_parses = {}
        pagination_limit = current_app.config.get('PAGINATION_LIMIT', 25)
        # some common get query
        self.add_argument('common', 'lang', str, help='specified language')

        self.add_argument('get', 'q', str, help='query string')
        self.add_argument('get', 'offset', NumberRange(min=0), default=0, help='offset pagination')
        self.add_argument('get', 'limit', NumberRange(min=1, max=pagination_limit),
                          default=pagination_limit, help='limit pagination')
        self.add_argument('get', 'sort', str, help='sorting')
        self.add_argument('get', 'one', boolean, help='expect only one result')

        self.add_argument('post', '_method', str,
                          help='POST method with a client having limited http method support')

    def add_argument(self, method, name, a_type, required=False, location=None,
                     default=None, help=None, **kwargs):
        """Add argument for request parser"""
        kwargs['name'] = name
        kwargs['type'] = a_type
        kwargs['required'] = required
        _add_if_not_none(kwargs, 'location', location)
        _add_if_not_none(kwargs, 'default', default)
        _add_if_not_none(kwargs, 'help', help)

        if self.req_parses.get(method) is None:
            self.req_parses[method] = RequestParser(trim=True)

        self.req_parses[method].add_argument(**kwargs)

    def parse_arguments(self, method=None, ignored_values=(None, ''), **kwargs):
        """Parse the request for arguments"""
        filters = []
        common_args = self.req_parses['common'].parse_args(**kwargs)
        common_args = extract_dict(common_args, ignored_values=ignored_values)
        method = method or request.method.lower()

        if self.req_parses.get(method) is None:
            return common_args
        args = self.req_parses[method].parse_args(**kwargs)

        # it's assumed that 'common' will not include any filter query
        # parse filters ?field__op=value => convert to [{key: field, op: op, value:value}, ]
        filter_dict = extract_dict(args, func=lambda k, v: FILTER_KEY_REGEX.match(k))

        for key, value in filter_dict.iteritems():
            matcher = FILTER_KEY_REGEX.match(key)
            key = matcher.group('key')
            operator = matcher.group('op')

            if operator == 'in' or operator == 'ni':
                value = value.split(',')

            filters.append({
                'key': key,
                'op': SA_OPS_MAPPER.get(operator),
                'value': value
            })

        args = extract_dict(args, func=lambda k, v: not FILTER_KEY_REGEX.match(k))

        if len(filters) > 0:
            args['filters'] = filters

        common_args.update(extract_dict(args, ignored_values=ignored_values))
        return common_args


# Thanks to: https://gist.github.com/ratchit/3942066
class BaseResource(RequestParserResourceMixin, Resource):
    """The base resource
    """
    action_decorators = {}

    def dispatch_request(self, *args, **kwargs):
        """Derived Resource dispatch to allow for decorators to be
            applied to specific individual request methods - in addition
            to the standard decorator assignment.

            Example decorator use:
            decorators = [user_required] # applies to all methods, the same with `method_decorators`
            action_decorators = {
                'post': [admin_required, format_results]
            }
        """

        view = super(BaseResource, self).dispatch_request
        decorators = self.action_decorators.get(request.method.lower())
        if decorators:
            for decorator in decorators:
                view = decorator(view)

        return view(*args, **kwargs)


class TokenRequiredResource(BaseResource):
    """The base resource class that requires token authentication"""

    decorators = [token_auth_required()]


class AdminRoleRequiredResource(BaseResource):
    """The base resource class that requires admin role"""

    decorators = [roles_required('admin'), token_auth_required()]
