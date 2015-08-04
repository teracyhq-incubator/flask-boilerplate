# -*- coding: utf-8 -*-
"""application exceptions"""


class ApplicationException(Exception):
    """The top most application exception"""
    def __init__(self, message, code=None, description=None, more_info=None,
                 status_code=None, errors=None):
        self.message = message
        self.code = code
        self.description = description
        self.more_info = more_info
        self.errors = errors if errors else []
        self.status_code = status_code

    def to_json(self):
        error = {
            'code': self.code,
            'message': self.message,
            'description': self.description,
            'errors': self.errors,
            'more_info': self.more_info
        }
        if self.status_code is not None:
            error['status_code'] = self.status_code
        return {
            'error': error
        }


class BadRequestException(ApplicationException):

    def __init__(self, *args, **kwargs):
        kwargs['status_code'] = 400
        super(BadRequestException, self).__init__(*args, **kwargs)


class UnauthorizedException(ApplicationException):

    def __init__(self, *args, **kwargs):
        kwargs['status_code'] = 401
        super(UnauthorizedException, self).__init__(*args, **kwargs)


class ForbiddenException(ApplicationException):

    def __init__(self, *args, **kwargs):
        kwargs['status_code'] = 403
        super(ForbiddenException, self).__init__(*args, **kwargs)


class NotFoundException(ApplicationException):

    def __init__(self, *args, **kwargs):
        kwargs['status_code'] = 404
        super(NotFoundException, self).__init__(*args, **kwargs)
