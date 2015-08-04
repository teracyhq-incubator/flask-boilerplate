# -*- coding:utf-8 -*-

"""unit tests for app"""

import os

from mock import patch

APP_TEST_PATH = os.path.abspath(os.path.dirname(__file__))


class CurrentAppMockMixin(object):

    def setUp(self):

        from app.config import TestConfig

        app_config = {key: getattr(TestConfig, key) for key in dir(TestConfig) if
                      not key.startswith('__') and not callable(key)}

        app_config['JWT_LEEWAY'] = 0
        app_config['JWT_SECRET_KEY'] = 'secret'
        app_config['JWT_ALGORITHM'] = 'HS256'

        self.base_current_app_patcher = patch('app.api.base.current_app')
        self.base_mock_current_app = self.base_current_app_patcher.start()
        self.base_mock_current_app.config = app_config

        self.auth_current_app_patcher = patch('app.api_1_0.auth.current_app')
        self.auth_mock_current_app = self.auth_current_app_patcher.start()
        self.auth_mock_current_app.config = app_config

    def tearDown(self):
        del self.base_mock_current_app
        self.base_current_app_patcher.stop()
        del self.base_current_app_patcher

        del self.auth_mock_current_app
        self.auth_current_app_patcher.stop()
        del self.auth_current_app_patcher
