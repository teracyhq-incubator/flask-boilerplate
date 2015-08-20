# -*- coding: utf-8 -*-

"""api v2.0"""

from flask import Blueprint, g

api_bp = Blueprint('api_1_0', __name__, url_prefix='/api/v1.0')


@api_bp.before_request
def before_request():
    g.token_auth_used = g.http_auth_used = None
    # FIXME(hoatle): security check of inactive, not verified users
    # TODO(hoatle): exclude debug toolbar for /api/, add rest logger to serve ?debug query
    # TODO(hoatle): session usage should be removed from REST

import errors

from .users import UserResource
from .token import TokenResource
from .roles import RoleResource

UserResource.register(api_bp)
TokenResource.register(api_bp)
RoleResource.register(api_bp)
