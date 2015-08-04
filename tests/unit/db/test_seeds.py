# -*- coding: utf-8 -*-

"""db.seeds tests"""

from mock import patch


from tests.unit import UnitTestCase


class SeedsTestCase(UnitTestCase):

    @patch('db.seeds.Role')
    def test_run(self, mock_role):
        from db import seeds

        seeds.run()

        mock_role.insert_roles.assert_called_once_with()
