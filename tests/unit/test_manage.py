# -*- coding: utf-8 -*-

"""tests for manage"""

from tests.unit import UnitTestCase

import manage


class ManageTestCase(UnitTestCase):
    """tests for manage"""

    def test_app(self):
        """tests for manage.app"""
        self.assertIsNotNone(manage.app, 'manage.app must not be None')

    def test_manager(self):
        """tests for manage.manager"""
        self.assertIsNotNone(manage.manager, 'manage.manager must not be None')
