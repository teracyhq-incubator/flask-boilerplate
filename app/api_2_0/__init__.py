# -*- coding: utf-8 -*-

"""api v2.0"""

from flask import Blueprint, g

api_bp = Blueprint('api_2_0', __name__, url_prefix='/api/v2.0')

@api_bp.before_request
def before_request():
    g.token_auth_used = g.http_auth_used = None
    # FIXME(hoatle): security check of inactive, not verified users
    # TODO(hoatle): exclude debug toolbar for /api/, add rest logger to serve ?debug query
    # TODO(hoatle): session usage should be removed from REST

import errors

from .users import UserAPI
from .token import TokenAPI
from .roles import RoleAPI

UserAPI.register(api_bp)
TokenAPI.register(api_bp)
RoleAPI.register(api_bp)
