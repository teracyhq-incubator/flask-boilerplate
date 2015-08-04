# -*- coding: utf-8 -*-

"""auth checkers"""

from flask import g
from flask_security import current_user
from flask_security.decorators import _check_http_auth
from flask_jwt import verify_jwt, JWTError


def verify_token_auth(realm=None):
    """verify token authentication

    :param realm:
    :return:
    """
    try:
        verify_jwt(realm)
    except JWTError:
        return False
    return True


def verify_http_auth():
    """verify http basic authentication

    :return:
    """
    return _check_http_auth()


#  FIXME(hoatle): inactive or not verified users (?) should be blocked
def token_authenticated():
    """check if the token authentication is used"""
    g.token_auth_used = verify_token_auth()
    return g.token_auth_used


#  FIXME(hoatle): inactive or not verified users (?) should be blocked
def http_authenticated():
    """check if the basic authentication is used"""
    g.http_auth_used = verify_http_auth()
    return g.http_auth_used


def session_authenticated():
    """check if the session authentication is used"""
    return current_user.is_authenticated() and not (g.token_auth_used or g.http_auth_used)


def authenticated():
    """check if the current user is authenticated"""
    return g.token_auth_used or g.http_auth_used or current_user.is_authenticated()
