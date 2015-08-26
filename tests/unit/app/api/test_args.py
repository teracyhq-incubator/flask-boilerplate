# -*- coding: utf-8 -*-

"""tests for app.api.args"""

from app.api.args import BoolArg

from tests.unit import UnitTestCase


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
