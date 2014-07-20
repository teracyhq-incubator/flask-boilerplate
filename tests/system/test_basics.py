# -*- coding: utf-8 -*-

from flask import current_app

from . import SystemTestCase


class BasicsTestCase(SystemTestCase):

    def test_app_exists(self):
        self.assertIsNotNone(current_app, 'current_app must not be None')
