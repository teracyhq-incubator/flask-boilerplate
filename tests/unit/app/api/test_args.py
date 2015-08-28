# -*- coding: utf-8 -*-

"""tests for app.api.args"""

from app.api.args import BoolArg

from tests.unit import UnitTestCase

from mock import patch


class ArgsTestCase(UnitTestCase):

    def test_bool_arg(self):

        tests = {
            'true': True,
            'True': True,
            'tRuE': True,
            'false': False,
            'False': False,
            'fAlSe': False,
            '0': False,
            '1': True,
            '-1': True,  # follow python bool
            'something': True
        }

        for val, expected in tests.iteritems():
            self.assertEqual(BoolArg.validated('active', val), expected,
                             '{} should be {}'.format(val, expected))

    @patch('app.api.args.use_args')
    def test_extract_args_class_method(self, mock_use_args):

        from app.api.args import extract_args

        search_args = {
        }

        def use_args(args):
            return args

        mock_use_args.return_value = use_args


        # class method
        class Test:
            @extract_args(search_args)
            def test(self, args, **kwargs):
                return args

        test = Test()


        # missing value
        result = test.test({
            'email': 'test@email.com',
            'def__lt': '2.3'
        })

        

        expected_result = {
            'email': 'test@email.com',
            'filters': [
                {'key': 'def', 'op': 'lt', 'value': 2.3}
            ]
        }


        self.assertEqual(result, expected_result)


        # correct format
        result = test.test({
            'name': 'sample',
            'abc__eq': '1',
            'def__lt': '2',
            'a__bc': 'def',
        })

        expected_result = {
            'name': 'sample',
            'a__bc': 'def',
            'filters': [
                {'key': 'def', 'op': 'lt', 'value': 2},
                {'key': 'abc', 'op': 'eq', 'value': 1}
            ]
        }

        self.assertEqual(result, expected_result)


        # contain quote
        result = test.test({
            'name': 'sample',
            'abc__eq': '1',
            'def__lt': '"3"',
        })

        expected_result = {
            'name': 'sample',
            'filters': [
                {'key': 'def', 'op': 'lt', 'value': '"3"'},
                {'key': 'abc', 'op': 'eq', 'value': 1},
            ]
        }

        self.assertEqual(result, expected_result)

        # contain list
        result = test.test({
            'name': 'sample',
            'abc__in': '1,2,3,t',
        })

        expected_result = {
            'name': 'sample',
            'filters': [
                {'key': 'abc', 'op': 'in_', 'value': [1,2,3,'t']},
            ]
        }

        self.assertEqual(result, expected_result)

    @patch('app.api.args.use_args')
    def test_extract_args_single_function(self, mock_use_args):

        from app.api.args import extract_args

        search_args = {
        }

        def use_args(args):
            return args

        mock_use_args.return_value = use_args

        # function
        # @extract_args(search_args)
        # def test_1_arg(args):
        #     return args

        @extract_args(search_args)
        def test_2_arg(obj, args):
            return args

        # result1 = test_1_arg({
        #     'name': 'sample',
        #     'abc__eq': '1',
        #     'def__lt': '"3"',
        #     'ghi__in': 'abc,def',
        # })

        result2 = test_2_arg(None, {
            'name': 'sample',
            'abc__eq': '1',
            'def__lt': '"3"',
            'ghi__in': 'abc,def',
        })

        expected_result = {
            'name': 'sample',
            'filters': [
                {'key': 'def', 'op': 'lt', 'value': '"3"'},
                {'key': 'ghi', 'op': 'in_', 'value': ['abc', 'def']},
                {'key': 'abc', 'op': 'eq', 'value': 1},
            ]
        }

        # self.assertEqual(result1, expected_result)
        self.assertEqual(result2, expected_result)


