# -*- coding: utf-8 -*-

"""decorators for api resources"""

from functools import wraps

from flask import current_app, _request_ctx_stack
from flask_principal import Identity, identity_changed
from flask_jwt import current_user, verify_jwt
from webargs.flaskparser import use_args

from ..auth import (permissions_required as auth_permissions_required,
                    permissions_accepted as auth_permissions_accepted,
                    roles_required as auth_roles_required,
                    roles_accepted as auth_roles_accepted)
from ..exceptions import ApplicationException, UnauthorizedException, BadRequestException
from ..pagination import OffsetPagination
from . import (authenticated, token_authenticated, http_authenticated,
               session_authenticated)
from .utils import extract_filters


def anonymous_required(func):
    """Decorator that requires the user client must be anonymous."""

    @wraps(func)
    def decorated(*args, **kwargs):
        if authenticated():
            raise BadRequestException(
                'Not Anonymous',
                description='the request is authenticated but anonymous is required'
            )
        return func(*args, **kwargs)

    return decorated


def token_auth_required(realm=None):
    """Decorator that requires a valid JWT token to be present in the request

    :param realm: an optional realm
    """

    def wrapper(func):
        @wraps(func)
        def decorated(*args, **kwargs):
            verify_jwt(realm)
            if current_user and current_user.is_authenticated():
                app = current_app._get_current_object()
                _request_ctx_stack.top.user = current_user
                identity_changed.send(app, identity=Identity(current_user.id))
                return func(*args, **kwargs)
            raise UnauthorizedException('Invalid Token', description='token is invalid')

        return decorated

    return wrapper


def http_auth_required(func):
    """Decorator that protects endpoints using basic authentication."""

    @wraps(func)
    def decorated(*args, **kwargs):
        if http_authenticated():
            return func(*args, **kwargs)
        raise UnauthorizedException(
            'Invalid Basic Authentication',
            description='basic authentication was invalid or not provided'
        )

    return decorated


def session_auth_required(func):
    """Decorator that protects endpoints using session authentication.
    Normally, we don't use this, just make it here the same support as flask-security"""

    @wraps(func)
    def decorated(*args, **kwargs):
        if session_authenticated():
            return func(*args, **kwargs)
        raise UnauthorizedException(
            'Invalid Session Authentication',
            description='session authentication was invalid or not provided'
        )

    return decorated


# TODO(hoatle): consider to rename this to: `auth_accepted` to make it consistent with others
# decorators?
def auth_required(*auth_methods):
    """
    Decorator that protects end points through multiple mechanisms, when a mechanism is passed, then
    the decorator is passed.
    Example::

        @api.resource('/users', endpoint='users')
        class UserListAPI(BaseResource):
            action_decorators = {
                'get': [auth_required('token', 'basic')]
            }

            def get(self):
                return {'users': User.query.all()}

    :param auth_methods: Specified mechanisms.
    """
    login_mechanisms = {
        'token': token_authenticated,
        'basic': http_authenticated,
        'session': session_authenticated
    }

    def wrapper(func):
        @wraps(func)
        def decorated(*args, **kwargs):
            mechanisms = [login_mechanisms.get(method) for method in auth_methods]
            for mechanism in mechanisms:
                if mechanism and mechanism():
                    return func(*args, **kwargs)

            raise UnauthorizedException(
                'Invalid Authentication',
                description='required {} authentication was invalid or not provided'.
                format(' or '.join(auth_methods))
            )

        return decorated

    return wrapper


def permissions_required(*permissions):
    def exception_handler(permission):
        raise UnauthorizedException(
            'Invalid Permission',
            description='required {} permission was invalid or not provided'.
            format(str(permission))
        )

    return auth_permissions_required(*permissions, exception_handler=exception_handler)


def permissions_accepted(*permissions):
    def exception_handler(perms):
        raise UnauthorizedException(
            'Invalid Permission',
            description='required {} permission was invalid or not provided'.
            format(' or '.join([str(x) for x in perms]))
        )

    return auth_permissions_accepted(*permissions, exception_handler=exception_handler)


def roles_required(*roles):
    """Decorator which specifies that a user must have all the specified roles.
    Example::

        @api.resource('/posts', endpoint='posts')
        class PostListAPI(BaseResource):
            action_decorators = {
                'post': [auth_required('token'), roles_required('admin', 'editor')]
            }

            def post(self):
                return {}, 201

    The current user must have both the `admin` role and `editor` role in order
    to create a new post.

    :param args: The required roles.
    """

    def exception_handler(permission):
        raise UnauthorizedException(
            'Invalid Permission',
            description='required {} permission was invalid or not provided'.
            format(str(permission))
        )

    return auth_roles_required(*roles, exception_handler=exception_handler)


def roles_accepted(*roles):
    """Decorator which specifies that a user must have at least one of the
    specified roles. Example::

         @api.resource('/posts', endpoint='posts')
         class PostListAPI(BaseResource):
            action_decorators = {
                'put': [auth_required('token'), roles_accepted('editor', 'author')]
            }

            def put(self):
                return {}, 200

    The current user must have either the `editor` role or `author` role in
    order to update the post.

    :param args: The possible roles.
    """

    def exception_handler(permissions):
        raise UnauthorizedException(
            'Invalid Permission',
            description='required {} permission was invalid or not provided'.
            format('or '.join([str(x) for x in permissions]))
        )

    return auth_roles_accepted(*roles, exception_handler=exception_handler)


def one_of(*decorators):
    """Decorator helper to make sure one of the decorators must pass (no exception thrown)
    Example::

        @api.resource('/users', endpoint='users')
        class UserListAPI(BaseResource):
            action_decorators = {
                'post': [one_of(anonymous_required, roles_required('admin'))]
            }

            def post(self):
                return {}, 201

    The current user must be anonymous user or admin user in order
    to create a new user.

    :param decorators: The decorators.
    """

    def wrapper(func):
        @wraps(func)
        def decorated(*args, **kwargs):
            exs = []
            for idx, decorator in enumerate(decorators):
                try:
                    result = decorator(func)(*args, **kwargs)
                    return result
                except Exception as ex:
                    if idx == (len(decorators) - 1):
                        if not isinstance(ex, ApplicationException):
                            # dirty hack of ex.error
                            ex = ApplicationException(ex.message or getattr(ex, 'error', None),
                                                      description='')
                        for e in exs:
                            if not isinstance(e, ApplicationException):
                                e = ApplicationException(e.message or getattr(e, 'error', None) or
                                                         getattr(e, 'name', None),
                                                         description=getattr(e, 'data', None) or '')
                            ex.message += ' or {}'.format(e.message) \
                                if e.message is not None else ''
                            ex.description += ' or {}'.format(e.description) \
                                if ex.description and e.description \
                                else '{}'.format(e.description or '')
                        raise ex
                    exs.append(ex)
            return func(*args, **kwargs)

        return decorated

    return wrapper


def paginated(func):
    """paginated decorator to display the list of items from the query returned by the
    decorated function
    """

    @wraps(func)
    def decorated(*args, **kwargs):
        query, args_dict = func(*args, **kwargs)

        if args_dict.get('one', False) is True:
            data = [query.one()]
            paging = {
                'count': 1,
                'offset': 0,
                'limit': 1,
                'previous': None,
                'next': None
            }
        else:
            pagination = OffsetPagination(query,
                                          offset=args_dict.get('offset', None),
                                          limit=args_dict.get('limit', None))
            data = pagination.data
            paging = {
                'count': pagination.count,
                'offset': pagination.offset,
                'limit': pagination.limit,
                'previous': pagination.prev_url,
                'next': pagination.next_url
            }

        return {
            'data': data,
            'paging': paging
        }

    return decorated


def extract_args(arg_map, req=None, locations=None, as_kwargs=False, validate=None):

    def wrapper(func):

        @wraps(func)
        @use_args(arg_map, req=req, locations=locations, as_kwargs=as_kwargs, validate=validate)
        def decorated(resource, req_args, *args, **kwargs):
            filters, req_args = extract_filters(req_args)
            req_args['filters'] = filters

            return func(resource, req_args, *args, **kwargs)

        return decorated
    return wrapper
