# -*- coding: utf-8 -*-

"""tests for api.validators"""
from mock import MagicMock

from tests.unit import UnitTestCase
from app.api.validators import DummyForm, DummyField, Base, password


class DummyFormTestCase(UnitTestCase):

    def test_class(self):
        self.assertTrue(issubclass(DummyForm, dict))


class DummyFieldTestCase(UnitTestCase):

    def test_init(self):
        dummy_field = DummyField(None)
        self.assertEqual(dummy_field.data, None)
        self.assertEqual(dummy_field.errors, [])
        self.assertEqual(dummy_field.raw_data, None)

        dummy_field = DummyField('a', ('something wrong', ), 'a   ')
        self.assertEqual(dummy_field.data, 'a')
        self.assertEqual(dummy_field.errors, ['something wrong'])
        self.assertEqual(dummy_field.raw_data, 'a   ')

    def test_gettext(self):

        dummy_field = DummyField('a')

        self.assertEqual(dummy_field.gettext('hello'), 'hello')
        self.assertEqual(dummy_field.gettext(None), None)

    def test_ngettext(self):
        dummy_field = DummyField('a')

        self.assertEqual(dummy_field.ngettext('one', 'many', 1), 'one')
        self.assertEqual(dummy_field.ngettext('one', 'many', 2), 'many')


class BaseTestCase(UnitTestCase):

    def test_init(self):
        mock_validator_class = MagicMock()

        mock_validator_class.return_value = 'validator'

        base = Base(mock_validator_class, 'a', message='hello')

        mock_validator_class.assert_called_once_with('a', message='hello')
        self.assertEqual(base.validator, 'validator')

    def test_call(self):
        mock_validator = MagicMock()
        mock_validator_class = MagicMock(return_value=mock_validator)

        value = Base(mock_validator_class)('test')
        self.assertEqual(mock_validator.call_count, 1)
        self.assertEqual(value, 'test')


class LengthTestCase(UnitTestCase):

    def test_init(self):
        from app.api.validators import Length, wtf_length

        self.assertRaises(AssertionError, Length)
        self.assertRaises(AssertionError, Length, min=3, max=2)

        length_validator = Length(min=0, max=5, message='something wrong')
        validator = length_validator.validator
        self.assertTrue(isinstance(validator, wtf_length))
        self.assertEqual(validator.min, 0)
        self.assertEqual(validator.max, 5)
        self.assertEqual(validator.message, 'something wrong')


class NumberRangeTestCase(UnitTestCase):

    def test_init(self):
        from app.api.validators import NumberRange, wtf_number_range

        number_range_validator = NumberRange(min=0, max=5, message='something wrong')

        validator = number_range_validator.validator
        self.assertTrue(isinstance(validator, wtf_number_range))
        self.assertEqual(validator.min, 0)
        self.assertEqual(validator.max, 5)
        self.assertEqual(validator.message, 'something wrong')

    def test_call(self):

        from app.api.validators import NumberRange

        number_range_validator = NumberRange(min=0, max=5)
        self.assertEqual(number_range_validator('0'), 0)
        self.assertEqual(number_range_validator('5'), 5)

        self.assertRaises(ValueError, number_range_validator, 6)
        self.assertRaises(ValueError, number_range_validator, '-1')


class EmailTestCase(UnitTestCase):

    def test_init(self):

        from app.api.validators import Email, wtf_email

        email_validator = Email(message='something wrong')
        validator = email_validator.validator

        self.assertTrue(isinstance(validator, wtf_email))
        self.assertEqual(validator.message, 'something wrong')


class IPAddressTestCase(UnitTestCase):

    def test_init(self):

        from app.api.validators import IPAddress, wtf_ip_address

        ip_address_validator = IPAddress(ipv4=False, ipv6=True, message='something wrong')
        validator = ip_address_validator.validator

        self.assertTrue(isinstance(validator, wtf_ip_address))
        self.assertFalse(validator.ipv4)
        self.assertTrue(validator.ipv6)
        self.assertEqual(validator.message, 'something wrong')


class MacAddressTestCase(UnitTestCase):

    def test_init(self):

        from app.api.validators import MacAddress, wtf_mac_address

        mac_address_validator = MacAddress(message='something wrong')
        validator = mac_address_validator.validator

        self.assertTrue(isinstance(validator, wtf_mac_address))
        self.assertEqual(validator.message, 'something wrong')


class AnyOfTestCase(UnitTestCase):

    def test_init(self):

        from app.api.validators import AnyOf, wtf_any_of

        formatter = lambda x: x

        any_of_validator = AnyOf([1, 3, 5], message='something wrong', values_formatter=formatter)
        validator = any_of_validator.validator

        self.assertTrue(isinstance(validator, wtf_any_of))
        self.assertEqual(validator.values, [1, 3, 5])
        self.assertEqual(validator.message, 'something wrong')
        self.assertEqual(validator.values_formatter, formatter)


class NoneOfTestCase(UnitTestCase):

    def test_unit(self):

        from app.api.validators import NoneOf, wtf_none_of

        formatter = lambda x: x

        none_of_validator = NoneOf([1, 3, 5], message='something wrong', values_formatter=formatter)
        validator = none_of_validator.validator

        self.assertTrue(isinstance(validator, wtf_none_of))
        self.assertEqual(validator.values, [1, 3, 5])
        self.assertEqual(validator.message, 'something wrong')
        self.assertEqual(validator.values_formatter, formatter)


class ValidatorsTestCase(UnitTestCase):

    def test_password(self):

        too_short_msg = 'password too short, length must be greater than 6'
        space_contained_msg = 'password must not contain space(s)'

        password_check_list = (
            ('a', False, too_short_msg),
            ('abcde', False, too_short_msg),
            ('       ', False, space_contained_msg),
            ('a bcdefgh', False, space_contained_msg),
            (' abcde', False, space_contained_msg),
            ('abcdef', True, None),
            ('  abcdef  ', False, space_contained_msg),
        )

        for pwd, correct, msg in password_check_list:
            if correct:
                self.assertEqual(password(pwd), pwd)
            else:
                with self.assertRaises(ValueError) as ve:
                    password(pwd)
                self.assertEqual(ve.exception.message, msg, 'with the case of `{}`'.format(pwd))
