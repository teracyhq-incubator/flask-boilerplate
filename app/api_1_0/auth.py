# -*- coding: utf-8 -*-

"""api v1.0 auth"""

from datetime import timedelta
import math

from flask import g, current_app
from flask_security import current_user

from ..api import (http_auth_required, token_auth_required, BaseResource,
                   jwt_make_payload, jwt_encode_payload, jwt_authenticate, one_of)
from ..api.validators import Email, password, NumberRange
from ..exceptions import BadRequestException
from . import api, api_bp


@api_bp.before_request
def before_request():
    g.token_auth_used = g.http_auth_used = None
    # FIXME(hoatle): security check of inactive, not verified users
    # TODO(hoatle): exclude debug toolbar for /api/, add rest logger to serve ?debug query
    # TODO(hoatle): session usage should be removed from REST


@api.resource('/token', endpoint='token')
class TokenAPI(BaseResource):
    """Serve requests for the authentication token."""

    action_decorators = {
        'get': [one_of(token_auth_required(), http_auth_required)]
        # 'post': [anonymous_required] # TODO(hoatle): required?
    }

    @staticmethod
    def _token_result(user, expires_in=None):
        expiration_delta = timedelta(seconds=expires_in) if expires_in else None
        payload = jwt_make_payload(user, expiration_delta=expiration_delta)
        expires_in = int(math.floor((payload['exp'] - payload['iat']).total_seconds()))
        return {
            'token': jwt_encode_payload(payload),
            'expires_in': expires_in  # The number of seconds until this access token expires
        }

    def __init__(self):
        super(TokenAPI, self).__init__()
        self.add_argument('post', 'email', Email(), required=True, help='user email')
        self.add_argument('post', 'password', password, required=True, help='user password')

        min_expires_in = current_app.config.get('JWT_MIN_EXPIRES_IN')
        max_expires_in = current_app.config.get('JWT_MAX_EXPIRES_IN')
        self.add_argument('common', 'expires_in', NumberRange(min_expires_in, max_expires_in),
                          help='number of seconds until this access token expires')

    def get(self):
        """
        /api/vx.x/token should be requested get new authentication token by basic authentication
        (username + password) header or by existing token, by using this client app could get
        a new token.
        After having a token, clients must use this authentication_token for accessing other
        resources.
        """
        args = self.parse_arguments()
        return self._token_result(current_user, args.get('expires_in'))

    def post(self):
        """Login and return JWT token
        """
        args = self.parse_arguments()
        user = jwt_authenticate(args.get('email'), args.get('password'))
        if user:
            return self._token_result(user, args.get('expires_in'))

        raise BadRequestException(
            'Invalid Credentials',
            description='email or password is not correct'
        )
