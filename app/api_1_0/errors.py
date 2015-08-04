# -*- coding: utf-8 -*-

"""api v1.0 error handlers"""

from flask import request, jsonify, render_template
from sqlalchemy.exc import SQLAlchemyError
from jwt.exceptions import InvalidTokenError

from ..api.errors import api_exception_handler
from ..exceptions import ApplicationException, NotFoundException, BadRequestException
from . import api_bp


api_bp.errorhandler(ApplicationException)(api_exception_handler)


@api_bp.errorhandler(ValueError)
def value_error_handler(ex):
    """Register error handler for ValueError"""
    ex = BadRequestException('Something Wrong',
                             description=ex.message)
    return api_exception_handler(ex)


@api_bp.errorhandler(SQLAlchemyError)
def sql_alchemy_error_handler(ex):
    """Register error handler for SQLAlchemyError"""
    ex = BadRequestException('Something Wrong',
                             description=ex.message)
    return api_exception_handler(ex)


@api_bp.errorhandler(InvalidTokenError)
def invalid_token_error_handler(ex):
    """Register error handler for InvalidTokenError"""
    ex = BadRequestException('Something Wrong',
                             description=ex.message)
    return api_exception_handler(ex)


@api_bp.app_errorhandler(404)
def error_handler(ex):
    """Register error handler for 404"""
    if request.path.startswith('/api/'):  # FIXME(hoatle): hard-code
        ex = NotFoundException('Not Found',
                               description="'{}' path not found".format(request.full_path))
        return api_exception_handler(ex)

    return render_template('404.html'), ex.code
