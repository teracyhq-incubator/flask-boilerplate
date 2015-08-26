import math
from datetime import timedelta

from flask import current_app
from flask_security import current_user
from webargs import Arg
from webargs.flaskparser import parser

from .. import utils
from ..api import (Resource, one_of, token_auth_required, http_auth_required, jwt_make_payload,
                   jwt_encode_payload, jwt_authenticate)
from ..api.validators import NumberRange, Email, password
from ..exceptions import BadRequestException

_user_args = {
    'email': Arg(str, validate=Email, required=True),
    'password': Arg(str, validate=password, required=True)
}


class TokenResource(Resource):
    route_base = 'token'

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
        self.common_args = {}

    def before_request(self, name):
        min_expires_in = current_app.config.get('JWT_EXPIRES_IN_MIN')
        max_expires_in = current_app.config.get('JWT_EXPIRES_IN_MAX')

        self.common_args = {
            'expires_in': Arg(int, validate=NumberRange(min_expires_in, max_expires_in))
        }

    @one_of(http_auth_required, token_auth_required())
    def show(self):
        """
        /api/vx.x/token should be requested get new authentication token by basic authentication
        (username + password) header or by existing token, by using this client app could get
        a new token.
        After having a token, clients must use this authentication_token for accessing other
        resources.
        """
        args = parser.parse(self.common_args)
        return self._token_result(current_user, args.get('expires_in'))

    def create(self):
        """Login and return JWT token
        """
        args = parser.parse(utils.merge_dict(_user_args, self.common_args))
        user = jwt_authenticate(args.get('email'), args.get('password'))
        if user:
            # TODO(hoatle): support to make response from dict
            return self._token_result(user, args.get('expires_in'))

        raise BadRequestException(
            'Invalid Credentials',
            description='email or password is not correct'
        )
