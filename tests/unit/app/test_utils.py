# -*- coding: utf-8 -*-

"""tests for app.utils"""
from mock import MagicMock

from tests.unit import UnitTestCase
from app import utils


class UtilsTestCase(UnitTestCase):

    def test_instance_folder_path(self):
        self.assertIsNotNone(utils.INSTANCE_FOLDER_PATH,
                             'utils.INSTANCE_FOLDER_PATH must not be None')
        self.assertEqual(utils.INSTANCE_FOLDER_PATH, '/tmp/instance',
                         'utils.INSTANCE_FOLDER_PATH must be {}'.format('/tmp/instance'))

    def test_merge_dict(self):
        result = utils.merge_dict({'a': 1}, {'b': 2})
        self.assertEqual(result, {'a': 1, 'b': 2})

        result = utils.merge_dict({'c': 3}, None)
        self.assertEqual(result, {'c': 3})

        self.assertRaises(TypeError, utils.merge_dict, {'d': 4}, ['a', 'b'])

    def test_extract_dict_invalid(self):

        with self.assertRaises(ValueError) as ve:
            utils.extract_dict(None)
        self.assertEqual(ve.exception.message, 'origin_dict must be a dict')

        with self.assertRaises(ValueError) as ve:
            utils.extract_dict({}, extracted_keys=1)
        self.assertEqual(ve.exception.message, 'extracted_keys must be a sequence')

        with self.assertRaises(ValueError) as ve:
            utils.extract_dict({}, ignored_keys=2)
        self.assertEqual(ve.exception.message, 'ignored_keys must be a sequence')

        with self.assertRaises(ValueError) as ve:
            utils.extract_dict({}, ignored_values=3)
        self.assertEqual(ve.exception.message, 'ignored_values must be a sequence')

        with self.assertRaises(ValueError) as ve:
            utils.extract_dict({}, func=4)
        self.assertEqual(ve.exception.message, 'func must be a function')

    def test_extract_dict_origin_dict(self):

        self.assertEqual(utils.extract_dict({}), {})

        origin_dict = {
            'a': 1,
            'b': 2,
            'c': 3,
            'd': 4,
            'e': 5
        }
        expected_dict = origin_dict
        self.assertEqual(utils.extract_dict(origin_dict), expected_dict)

    def test_extract_dict_extracted_keys(self):
        origin_dict = {
            'a': 1,
            'b': 2,
            'c': 3,
            'd': 4,
            'e': 5
        }

        expected_dict = {
            'a': 1,
            'b': 2,
            'c': 3
        }

        extracted_keys = ('a', 'b', 'c')

        self.assertEqual(utils.extract_dict({}, extracted_keys=extracted_keys), {})

        self.assertEqual(utils.extract_dict(origin_dict, extracted_keys=extracted_keys),
                         expected_dict)

    def test_extract_dict_ignored_keys(self):
        origin_dict = {
            'a': 1,
            'b': 2,
            'c': 3,
            'd': 4,
            'e': 5
        }

        expected_dict = {
            'd': 4,
            'e': 5
        }

        ignored_keys = ('a', 'b', 'c')

        self.assertEqual(utils.extract_dict({}, ignored_keys=ignored_keys), {})

        self.assertEqual(utils.extract_dict(origin_dict, ignored_keys=ignored_keys), expected_dict)

    def test_extract_dict_ignored_values(self):
        origin_dict = {
            'a': 1,
            'b': 2,
            'c': 3,
            'd': 4,
            'e': 5
        }

        expected_dict = {
            'b': 2,
            'd': 4
        }

        ignored_values = (1, 3, 5)

        self.assertEqual(utils.extract_dict({}, ignored_values=ignored_values), {})

        self.assertEqual(utils.extract_dict(origin_dict, ignored_values=ignored_values),
                         expected_dict)

    def text_extract_dict_func(self):

        origin_dict = {
            'a': 1,
            'b': 2,
            'c': 3,
            'd': 4,
            'e': 5
        }

        expected_dict = {
            'a': 1,
            'e': 5
        }

        def filter_func(key, value):
            if key in ('b', 'c') or value in (4,):
                return False
            return True

        self.assertEqual(utils.extract_dict({}, func=filter_func), {})

        self.assertEqual(utils.extract_dict(origin_dict, func=filter_func), expected_dict)

    def test_extract_dict_full(self):

        origin_dict = {
            'a': 1,
            'b': 2,
            'c': 3,
            'd': 4,
            'e': 5
        }

        expected_dict = {
            'a': 1,
            'e': 5
        }

        extracted_keys = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')
        ignored_keys = ('b', 'j', 'k', 'l', 'm')
        ignored_values = (3, 10, 20, 30)
        func = lambda key, value: False if key == 'd' else True

        self.assertEqual(
            utils.extract_dict({}, extracted_keys, ignored_keys, ignored_values, func),
            {}
        )

        self.assertEqual(
            utils.extract_dict(origin_dict, extracted_keys, ignored_keys, ignored_values, func),
            expected_dict
        )

    def test_add_filters_invalid(self):
        with self.assertRaises(ValueError) as ve:
            utils.add_filters(None, None, None)
        self.assertEqual(ve.exception.message, 'query must not be None')

        with self.assertRaises(ValueError) as ve:
            utils.add_filters(MagicMock(), None, None)
        self.assertEqual(ve.exception.message, 'op_list must be a sequence')

        with self.assertRaises(ValueError) as ve:
            utils.add_filters(MagicMock(), 2, None)
        self.assertEqual(ve.exception.message, 'op_list must be a sequence')

    def test_add_filers_accepted_keys(self):

        mock_query = MagicMock()
        op_list = [
            {
                'key': 'age',
                'op': 'ge',
                'value': 20
            }
        ]

        self.assertEqual(utils.add_filters(mock_query, op_list, None), mock_query)
        self.assertEqual(utils.add_filters(mock_query, op_list, []), mock_query)
        self.assertEqual(utils.add_filters(mock_query, op_list, ['name']), mock_query)
        self.assertFalse(mock_query.filter.called)

    def test_add_filters_query(self):
        mock_query = MagicMock()
        mock_model_class = MagicMock()
        mock_query.column_descriptions = [
            {
                'type': mock_model_class
            }
        ]
        mock_query_return = 'returned'
        mock_query.filter.return_value = mock_query_return

        op_sequence = [
            {
                'key': 'name',
                'op': 'eq',
                'value': 'test'
            }
        ]

        mock_model_class.name = None

        with self.assertRaises(ValueError) as ve:
            utils.add_filters(mock_query, op_sequence, ('name',))
        self.assertEqual(ve.exception.message, 'Invalid filter column: name')

        column_mock = MagicMock()
        del column_mock.eq
        del column_mock.eq_
        del column_mock.__eq__
        mock_model_class.name = column_mock

        with self.assertRaises(ValueError) as ve:
            utils.add_filters(mock_query, op_sequence, ['name'])
        self.assertEqual(ve.exception.message, 'Invalid filter operator: eq')

        mock_eq = MagicMock()
        column_mock.__eq__ = mock_eq

        query = utils.add_filters(mock_query, op_sequence, ['name'])

        mock_eq.assert_called_once_with('test')
        mock_query.filter.assert_called_once_with(mock_eq('test'))
        self.assertEqual(query, mock_query_return)
