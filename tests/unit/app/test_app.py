# -*- coding: utf-8 -*-

"""tests app package"""

import os
import unittest

from app import create_app
from app.config import BaseConfig

from . import APP_TEST_PATH


class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    TEST_KEY = 'test'


class AppTestCase(unittest.TestCase):

    def test_create_app_default(self):
        created_app = create_app()
        self.assertIsNotNone(created_app, 'created_app must not be None')
        self.assertEquals(created_app.instance_path, '/tmp/instance',
                          'created_app.instance_path must be {}'.format('/tmp/instance'))
        self.assertFalse(created_app.config.get('DEBUG'),
                         "created_app.config.get('DEBUG') must be False")
        self.assertFalse(created_app.config.get('TESTING'),
                         "created_app.config.get('TESTING') must be False")

    def test_create_app_config(self):
        created_app = create_app(TestConfig)

        self.assertTrue(created_app.config.get('DEBUG'),
                        "created_app.config.get('DEBUG') must be True")
        self.assertTrue(created_app.config.get('TESTING'),
                        "created_app.config.get('TESTING') must be True")
        self.assertEquals(created_app.config.get('TEST_KEY'), 'test',
                          "created_app.config.get('TEST_KEY') must be equal to {}".format('test'))

        # 'dev' string config
        created_app = create_app('dev')
        self.assertTrue(created_app.config.get('DEBUG'),
                        "created_app.config.get('DEBUG') must be True")

        # 'test' string config
        created_app = create_app('test')
        self.assertTrue(created_app.config.get('TESTING'),
                        "created_app.config.get('TESTING') must be True")

        # configuration from a file, useful for stag and prod deployment
        stag_file = os.path.join(APP_TEST_PATH, 'resources', 'stag.cfg')

        created_app = create_app(stag_file)
        self.assertTrue(created_app.config.get('STAGING'),
                        "created_app.config.get('STAGING') must be True")

        prod_file = os.path.join(APP_TEST_PATH, 'resources', 'prod.py')

        created_app = create_app(prod_file)
        self.assertTrue(created_app.config.get('PRODUCTION'),
                        "created_app.config.get('PRODUCTION') must be True")

    def test_create_app_instance_folder_path(self):
        """test create_app with instance_folder_path and prod.py"""
        config_file = 'prod.py'
        instance_folder_path = os.path.join(APP_TEST_PATH, 'resources')

        created_app = create_app(config_file, instance_folder_path)

        self.assertTrue(created_app.config.get('PRODUCTION'),
                        "created_app.config.get('PRODUCTION') must be True")

    def test_create_app_config_file_not_exists(self):
        config_file = 'not-exists.cfg'
        with self.assertRaises(IOError):
            create_app(config_file)
