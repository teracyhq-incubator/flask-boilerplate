# -*- coding: utf-8 -*-

"""tests for api.fields"""
from flask_restful.fields import DateTime

from tests.unit import UnitTestCase
from app.api.fields import iso8601_datetime


class FieldsTestCase(UnitTestCase):

    def test_iso8061_datetime(self):
        self.assertTrue(isinstance(iso8601_datetime, DateTime),
                        'iso8601_datetime should be an instance of DateTime')
        self.assertEqual(iso8601_datetime.dt_format, 'iso8601',
                         'iso8601_datetime.dt_format should return "iso8601"')
