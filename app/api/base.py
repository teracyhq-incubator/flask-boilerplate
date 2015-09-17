# -*- coding: utf-8 -*-

"""base api"""

from functools import partial, wraps
from datetime import datetime, timedelta

import inflection
import jwt as jwt_lib
from werkzeug.security import safe_str_cmp
from flask import current_app,  make_response
from flask_security import utils, AnonymousUser
from flask_security.utils import md5
from flask_classy import FlaskView

from ..extensions import jwt, auth_datastore
from ..exceptions import ApplicationException
from .errors import api_exception_handler
from .decorators import token_auth_required, roles_required
from .representations.json import output_json


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
        max_expiration_delta = current_app.config['JWT_EXPIRATION_DELTA_MAX']
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


class Resource(FlaskView):
    """The base Resource class that other REST resources should extend from"""
    trailing_slash = False
    representations = {'application/json': output_json}

    special_methods = {
        'get': ['GET'],
        'put': ['PUT'],
        'patch': ['PATCH'],
        'post': ['POST'],
        'delete': ['DELETE'],
        'index': ['GET'],
        'create': ['POST'],
        'read': ['GET'],
        'update': ['PUT'],
        'list': ['GET']
    }

    @classmethod
    def get_route_base(cls):
        if cls.route_base is None:
            base_name = None
            if cls.__name__.endswith('API'):
                base_name = cls.__name__[:-3]
            elif cls.__name__.endswith('Resource'):
                base_name = cls.__name__[:-8]

            if base_name is not None:
                return inflection.dasherize(inflection.pluralize(inflection.underscore(base_name)))

        return super(Resource, cls).get_route_base()


    @classmethod
    def build_route_name(cls, method_name):

        if cls.__name__.endswith('API') or cls.__name__.endswith('Resource'):
            if cls.route_base is None:
                return cls.get_route_base() + ':%s' % method_name
            else:
                return cls.route_base + ':%s' % method_name

        return super(Resource, cls).build_route_name(method_name)


class TokenRequiredResource(Resource):
    """The base resource class that requires token authentication"""

    decorators = [token_auth_required()]


class AdminRoleRequiredResource(Resource):
    """The base resource class that requires admin role"""

    decorators = [roles_required('admin'), token_auth_required()]
