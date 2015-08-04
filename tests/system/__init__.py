"""system tests"""

import unittest

from nose.plugins.attrib import attr

from app import create_app


@attr('sys')
class SystemTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()
