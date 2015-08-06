# -*- coding: utf-8 -*-

"""auth decorators"""

from functools import wraps
import inspect

from flask import abort
from flask_principal import PermissionDenied, Permission, RoleNeed

def permissions_required(*permissions, **opt_kwargs):
    """Decorator which specifies that a user must have all the specified permissions.
    Example::

        @app.route('/users/:user_id')
        @permissions_required(user_permission, user_role_permission)
        def profile_view(user_id):
            return 'profile view'

    The current user must have *both* the user_id user permission and user role in order
    to view a specific profile.

    :param permissions: The required permissions.

    If the permission is a function, it will be called with action method args and kwargs
    """
    def wrapper(func):
        @wraps(func)
        def decorated(*args, **kwargs):
            for permission in permissions:
                if inspect.isfunction(permission):
                    permission = permission(args, kwargs)

                if not permission.can():
                    if opt_kwargs.get('http_exception'):
                        abort(opt_kwargs['http_exception'], permission)
                    if callable(opt_kwargs.get('exception_handler')):
                        return opt_kwargs.get('exception_handler')(permission)
                    raise PermissionDenied(permission)
            return func(*args, **kwargs)
        return decorated
    return wrapper


def permissions_accepted(*permissions, **opt_kwargs):
    """Decorator which specifies that a user must have at least one of the specified permissions.
    Example::

        @app.route('/users/:user_id/update')
        @permissions_accepted(user_permission, admin_role_permission)
        def profile_update(user_id):
            return 'profile update'

    The current user must have *one of* the user_id user permission or admin role in order
    to update a specific user.

    :param permissions: The accepted permissions.

    If the permission is a function, it will be called with action method args and kwargs
    """
    def wrapper(func):
        @wraps(func)
        def decorated(*args, **kwargs):
            for permission in permissions:
                if permission.can():
                    return func(*args, **kwargs)
            if opt_kwargs.get('http_exception'):
                abort(opt_kwargs['http_exception'], permissions)
            if callable(opt_kwargs.get('exception_handler')):
                return opt_kwargs.get('exception_handler')(permissions)
            raise PermissionDenied(permissions)
        return decorated
    return wrapper


def roles_accepted(*roles, **opt_kwargs):
    """Decorator which specifies that a user must have at least one of the
    specified roles.

    Example::

        @app.route('/create_post')
        @roles_accepted('editor', 'author')
        def create_post():
            return 'Create Post'

    The current user must have either the `editor` role or `author` role in
    order to view the page.

    :param roles: The possible role names.
    """
    perms = [Permission(RoleNeed(role)) for role in roles]
    return permissions_accepted(*perms, **opt_kwargs)


def roles_required(*roles, **opt_kwargs):
    """Decorator which specifies that a user must have all the specified roles.
    Example::

        @app.route('/dashboard')
        @roles_required('admin', 'editor')
        def dashboard():
            return 'Dashboard'

    The current user must have both the `admin` role and `editor` role in order
    to view the page.

    :param roles: The required role names.
    """
    perms = [Permission(RoleNeed(role)) for role in roles]
    return permissions_required(*perms, **opt_kwargs)
