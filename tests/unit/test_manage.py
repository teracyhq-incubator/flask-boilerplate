# -*- coding: utf-8 -*-

"""tests for manage"""

import unittest

import manage


class ManageTestCase(unittest.TestCase):

    def test_app(self):
        self.assertIsNotNone(manage.app, 'manage.app must not be None')

    def test_manager(self):
        self.assertIsNotNone(manage.manager, 'manage.manager must not be None')
