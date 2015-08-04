# -*- coding:utf-8 -*-

"""unit tests for mgr.migrate"""

from mock import patch
from tests.unit import UnitTestCase


class MigrateTestCase(UnitTestCase):

    @patch('mgr.migrate.drop')
    @patch('mgr.migrate.seeds')
    @patch('mgr.migrate.prompt_bool')
    @patch('mgr.migrate.create_database')
    @patch('mgr.migrate.database_exists')
    @patch('mgr.migrate.db')
    def test_setup_db_not_exists(self, mock_db, mock_database_exists, mock_create_database,
                                 mock_prompt_bool, mock_seeds, mock_drop):
        mock_database_exists.return_value = False
        mock_prompt_bool.return_value = False
        mock_db.engine.url = 'test'

        from mgr.migrate import setup

        setup()
        mock_database_exists.assert_called_once_with('test')
        mock_create_database.assert_called_once_with('test')
        mock_db.create_all.assert_called_once_with()
        mock_seeds.run.assert_called_once_with()
        self.assertEqual(mock_drop.call_count, 0, 'mock_drop.call_count should be 0')

    @patch('mgr.migrate.drop')
    @patch('mgr.migrate.seeds')
    @patch('mgr.migrate.prompt_bool')
    @patch('mgr.migrate.create_database')
    @patch('mgr.migrate.database_exists')
    @patch('mgr.migrate.db')
    def test_setup_db_exists(self, mock_db, mock_database_exists, mock_create_database,
                             mock_prompt_bool, mock_seeds, mock_drop):
        mock_database_exists.return_value = True

        mock_prompt_bool.return_value = False
        mock_db.engine.url = 'test'

        from mgr.migrate import setup

        setup()
        mock_database_exists.assert_called_once_with('test')
        mock_prompt_bool.assert_called_once_with(
            "'test' exists. Do you want to drop and create an empty one?")
        self.assertEqual(mock_prompt_bool.call_count, 1)
        self.assertEqual(mock_drop.call_count, 0, 'mock_drop.call_count should be 0')
        self.assertEqual(mock_create_database.call_count, 0)
        self.assertEqual(mock_db.create_all.call_count, 0)
        self.assertEqual(mock_seeds.run.call_count, 0)

        mock_prompt_bool.return_value = True
        setup()

        self.assertEqual(mock_database_exists.call_count, 2)
        self.assertEqual(mock_prompt_bool.call_count, 2)
        self.assertEqual(mock_drop.call_count, 1)
        self.assertEqual(mock_create_database.call_count, 1)
        self.assertEqual(mock_db.create_all.call_count, 1)
        self.assertEqual(mock_seeds.run.call_count, 1)

    @patch('mgr.migrate.seeds')
    def test_seed(self, mock_seeds):
        from mgr.migrate import seed
        seed()
        mock_seeds.run.assert_called_once_with()

    @patch('mgr.migrate.drop_database')
    @patch('mgr.migrate.database_exists')
    @patch('mgr.migrate.db')
    def test_drop_db_exists(self, mock_db, mock_database_exists, mock_drop_database):
        mock_database_exists.return_value = True
        mock_db.engine.url = 'test'

        from mgr.migrate import drop
        drop()

        mock_database_exists.assert_called_once_with('test')
        mock_drop_database.assert_called_once_with('test')

    @patch('mgr.migrate.drop_database')
    @patch('mgr.migrate.database_exists')
    @patch('mgr.migrate.db')
    def test_drop_db_not_exists(self, mock_db, mock_database_exists, mock_drop_database):
        mock_database_exists.return_value = False
        mock_db.engine.url = 'test'

        from mgr.migrate import drop
        drop()

        mock_database_exists.assert_called_once_with('test')
        self.assertFalse(mock_drop_database.called)

    @patch('mgr.migrate.setup')
    @patch('mgr.migrate.drop')
    def test_reset(self, mock_drop, mock_setup):
        from mgr.migrate import reset
        reset()
        mock_drop.assert_called_once_with()
        mock_setup.assert_called_once_with()
