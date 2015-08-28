
from tests.unit import UnitTestCase


class UtilsTestCase(UnitTestCase):

    def test_supported_ops(self):

        from app.api.utils import SUPPORTED_OPS

        supported_ops = ['eq', 'ne', 'lt', 'le', 'gt', 'ge', 'lk', 'nl', 'in', 'ni', 'ct', 'mc']

        for op in supported_ops:
            self.assertTrue(op in SUPPORTED_OPS, '{} should be in SUPPORTED_OPS'.format(op))

    def test_filter_key_re(self):

        from app.api.utils import FILTER_KEY_RE

        check_list = [
            ('name', False),
            ('name_', False),
            ('name__', False),
            ('_name_', False),
            ('name__ab', False),
            ('name__eq', True),
            ('_name__ne', True),
            ('a__ne', True),
            ('ab__lt', True),
            ('abc__le', True),
            ('def__gt', True),
            ('ghi__ge', True),
            ('jkl__lk', True),
            ('lmdd__nl', True),
            ('_ahoige__in', True),
            ('__dhoaihgeoiage__ni', True),
            ('ahgoiedadf__ct', True),
            ('nameddd__mc', True),
            ]

        for key, valid in check_list:
            if valid:
                self.assertTrue(FILTER_KEY_RE.match(key),
                                '{} should match {}'.format(key, FILTER_KEY_RE.pattern))
            else:
                self.assertFalse(FILTER_KEY_RE.match(key),
                                 '{} should not match {}'.format(key, FILTER_KEY_RE.pattern))

    def test_sq_ops_mapper(self):
        from app.api.utils import SA_OPS_MAPPER

        check_list = [
            ('eq', 'eq'),
            ('ne', 'ne'),
            ('lt', 'lt'),
            ('le', 'le'),
            ('gt', 'gt'),
            ('ge', 'ge'),
            ('lk', 'like'),
            ('nl', 'notlike'),
            ('in', 'in_'),
            ('ni', 'notin_'),
            ('ct', 'contains'),
            ('mc', 'match')
        ]

        for key, value in check_list:
            self.assertEqual(SA_OPS_MAPPER.get(key), value, '{} should match {}'.format(key, value))
