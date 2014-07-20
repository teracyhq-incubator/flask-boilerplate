# -*- coding: utf-8 -*-

"""tests for app.utils"""

from tests.unit import UnitTestCase
from app import utils


class UtilsTestCase(UnitTestCase):

    def test_instance_path(self):
        self.assertIsNotNone(utils.INSTANCE_FOLDER_PATH,
                             'utils.INSTANCE_FOLDER_PATH must not be None')
        self.assertEqual(utils.INSTANCE_FOLDER_PATH, '/tmp/instance',
                         'utils.INSTANCE_FOLDER_PATH must be {}'.format('/tmp/instance'))
