# -*- coding: utf-8 -*-

"""tests for app.exceptions"""

from tests.unit import UnitTestCase
from app.exceptions import (ApplicationException, BadRequestException, UnauthorizedException,
                            ForbiddenException, NotFoundException)


class ApplicationExceptionTestCase(UnitTestCase):

    def test_init(self):
        api_exception = ApplicationException('message')
        self.assertEqual(api_exception.message, 'message')
        self.assertEqual(api_exception.code, None)
        self.assertEqual(api_exception.description, None)
        self.assertEqual(api_exception.more_info, None)
        self.assertEqual(api_exception.status_code, None)

        api_exception = ApplicationException('message', 'E01')
        self.assertEqual(api_exception.message, 'message')
        self.assertEqual(api_exception.code, 'E01')

        api_exception = ApplicationException('message', code='E01')
        self.assertEqual(api_exception.message, 'message')
        self.assertEqual(api_exception.code, 'E01')

        api_exception = ApplicationException('message', 'E01', 'dev_message')
        self.assertEqual(api_exception.message, 'message')
        self.assertEqual(api_exception.code, 'E01')
        self.assertEqual(api_exception.description, 'dev_message')

        api_exception = ApplicationException('message', code='E01', description='dev_message')
        self.assertEqual(api_exception.message, 'message')
        self.assertEqual(api_exception.code, 'E01')
        self.assertEqual(api_exception.description, 'dev_message')

        api_exception = ApplicationException('message', 'E01', 'dev_message', 'more_info')
        self.assertEqual(api_exception.message, 'message')
        self.assertEqual(api_exception.code, 'E01')
        self.assertEqual(api_exception.description, 'dev_message')
        self.assertEqual(api_exception.more_info, 'more_info')

        api_exception = ApplicationException('message', code='E01', description='dev_message',
                                             more_info='more_info')
        self.assertEqual(api_exception.message, 'message')
        self.assertEqual(api_exception.code, 'E01')
        self.assertEqual(api_exception.description, 'dev_message')
        self.assertEqual(api_exception.more_info, 'more_info')

        api_exception = ApplicationException('message', 'E01', 'dev_message', 'more_info', 401)
        self.assertEqual(api_exception.message, 'message')
        self.assertEqual(api_exception.code, 'E01')
        self.assertEqual(api_exception.description, 'dev_message')
        self.assertEqual(api_exception.more_info, 'more_info')
        self.assertEqual(api_exception.status_code, 401)

        api_exception = ApplicationException('message', code='E01', description='dev_message',
                                             more_info='more_info', status_code=401)
        self.assertEqual(api_exception.message, 'message')
        self.assertEqual(api_exception.code, 'E01')
        self.assertEqual(api_exception.description, 'dev_message')
        self.assertEqual(api_exception.more_info, 'more_info')
        self.assertEqual(api_exception.status_code, 401)

    def test_to_json(self):

        api_exception = ApplicationException('message')
        result = {
            'error': {
                'code': None,
                'message': 'message',
                'description': None,
                'more_info': None,
                'errors': []
            }
        }
        self.assertEqual(api_exception.to_json(), result)

        api_exception = ApplicationException('message', status_code=402)
        result = {
            'error': {
                'code': None,
                'message': 'message',
                'description': None,
                'more_info': None,
                'errors': [],
                'status_code': 402
            }
        }
        self.assertEqual(api_exception.to_json(), result)

        api_exception = ApplicationException('message', code='E01', description='dev_message',
                                             more_info='more_info', status_code=401)
        result = {
            'error': {
                'code': 'E01',
                'message': 'message',
                'description': 'dev_message',
                'more_info': 'more_info',
                'errors': [],
                'status_code': 401
            }
        }

        self.assertEqual(api_exception.to_json(), result)


class BadRequestExceptionTestCase(UnitTestCase):

    def test_init(self):
        self.assertTrue(issubclass(BadRequestException, ApplicationException))
        exception = BadRequestException('something wrong')

        self.assertEqual(exception.message, 'something wrong',
                         'exception.message should be "something wrong"')
        self.assertEqual(exception.status_code, 400,
                         'exception.status_code should be 400')


class UnauthorizedExceptionTestCase(UnitTestCase):

    def test_init(self):
        self.assertTrue(issubclass(UnauthorizedException, ApplicationException))
        exception = UnauthorizedException('something wrong')

        self.assertEqual(exception.message, 'something wrong',
                         'exception.message should be "something wrong"')
        self.assertEqual(exception.status_code, 401,
                         'exception.status_code should be 401')


class ForbiddenExceptionTestCase(UnitTestCase):

    def test_init(self):
        self.assertTrue(issubclass(ForbiddenException, ApplicationException))
        exception = ForbiddenException('something wrong')

        self.assertEqual(exception.message, 'something wrong',
                         'exception.message should be "something wrong"')
        self.assertEqual(exception.status_code, 403,
                         'exception.status_code should be 403')


class NotFoundExceptionTestCase(UnitTestCase):

    def test_init(self):
        self.assertTrue(issubclass(NotFoundException, ApplicationException))
        exception = NotFoundException('something wrong')

        self.assertEqual(exception.message, 'something wrong',
                         'exception.message should be "something wrong"')
        self.assertEqual(exception.status_code, 404,
                         'exception.status_code should be 404')
