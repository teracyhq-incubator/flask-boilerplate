# -*- coding: utf-8 -*-

"""flask-restful validators
that extend https://github.com/flask-restful/flask-restful/blob/0.3.3/flask_restful/inputs.py

See:
- http://flask-restful.readthedocs.org/en/latest/extending.html#custom-fields-inputs
- https://github.com/wtforms/wtforms/blob/master/wtforms/validators.py
"""

from wtforms.validators import (email as wtf_email,
                                length as wtf_length,
                                number_range as wtf_number_range,
                                ip_address as wtf_ip_address,
                                mac_address as wtf_mac_address,
                                any_of as wtf_any_of,
                                none_of as wtf_none_of)

__all__ = ('Email', 'IPAddress', 'MacAddress', 'Length', 'NumberRange', 'AnyOf', 'NoneOf')


class DummyForm(dict):
    """Dummy form to leverage wtforms"""
    pass


class DummyField(object):
    """Dummy field to leverage wtforms"""
    # TODO(hoatle): add i18n support here
    def __init__(self, data, errors=(), raw_data=None):
        self.data = data
        self.errors = list(errors)
        self.raw_data = raw_data

    def gettext(self, string):
        return string

    def ngettext(self, singular, plural, n):
        if n == 1:
            return singular

        return plural


dummy_form = DummyForm()


class Base(object):
    """The base validator for other concrete validators to extend"""
    def __init__(self, validator_class, *args, **kwargs):
        self.validator = validator_class(*args, **kwargs)

    def __call__(self, value):
        self.validator(dummy_form, DummyField(value))
        return value


class Length(Base):
    """
    Validates the length of a string.

    :param min:
        The minimum required length of the string. If not provided, minimum
        length will not be checked.
    :param max:
        The maximum length of the string. If not provided, maximum length
        will not be checked.
    :param message:
        Error message to raise in case of a validation error. Can be
        interpolated using `%(min)d` and `%(max)d` if desired. Useful defaults
        are provided depending on the existence of min and max.
    """
    def __init__(self, min=-1, max=-1, message=None):
        kwargs = {
            'min': min,
            'max': max,
            'message': message
        }
        super(Length, self).__init__(wtf_length, **kwargs)


class NumberRange(Base):
    """
    Validates that a number is of a minimum and/or maximum value, inclusive.
    This will work with any comparable number type, such as floats and
    decimals, not just integers.

    :param min:
        The minimum required value of the number. If not provided, minimum
        value will not be checked.
    :param max:
        The maximum value of the number. If not provided, maximum value
        will not be checked.
    :param message:
        Error message to raise in case of a validation error. Can be
        interpolated using `%(min)s` and `%(max)s` if desired. Useful defaults
        are provided depending on the existence of min and max.
    """
    def __init__(self, min=None, max=None, message=None):
        kwargs = {
            'min': min,
            'max': max,
            'message': message
        }
        super(NumberRange, self).__init__(wtf_number_range, **kwargs)

    def __call__(self, value):
        value = int(value)
        return super(NumberRange, self).__call__(value)


class Email(Base):
    """
    Validates an email address. Note that this uses a very primitive regular
    expression and should only be used in instances where you later verify by
    other means, such as email activation or lookups.

    :param message:
        Error message to raise in case of a validation error.
    """
    def __init__(self, message=None):
        super(Email, self).__init__(wtf_email, **{'message': message})


class IPAddress(Base):
    """
    Validates an IP address.

    :param ipv4:
        If True, accept IPv4 addresses as valid (default True)
    :param ipv6:
        If True, accept IPv6 addresses as valid (default False)
    :param message:
        Error message to raise in case of a validation error.
    """
    def __init__(self, ipv4=True, ipv6=False, message=None):
        kwargs = {
            'ipv4': ipv4,
            'ipv6': ipv6,
            'message': message
        }
        super(IPAddress, self).__init__(wtf_ip_address, **kwargs)


class MacAddress(Base):
    """
    Validates a MAC address.

    :param message:
        Error message to raise in case of a validation error.
    """
    def __init__(self, message=None):
        super(MacAddress, self).__init__(wtf_mac_address, **{'message': message})


class AnyOf(Base):
    """
    Compares the incoming data to a sequence of valid inputs.

    :param values:
        A sequence of valid inputs.
    :param message:
        Error message to raise in case of a validation error. `%(values)s`
        contains the list of values.
    :param values_formatter:
        Function used to format the list of values in the error message.
    """
    def __init__(self, values, message=None, values_formatter=None):
        kwargs = {
            'message': message,
            'values_formatter': values_formatter
        }
        super(AnyOf, self).__init__(wtf_any_of, values, **kwargs)


class NoneOf(Base):
    """
    Compares the incoming data to a sequence of invalid inputs.

    :param values:
        A sequence of invalid inputs.
    :param message:
        Error message to raise in case of a validation error. `%(values)s`
        contains the list of values.
    :param values_formatter:
        Function used to format the list of values in the error message.
    """
    def __init__(self, values, message=None, values_formatter=None):
        args = (values,)
        kwargs = {
            'message': message,
            'values_formatter': values_formatter
        }
        super(NoneOf, self).__init__(wtf_none_of, *args, **kwargs)


# TODO(hoatle): define better password validator basing on the auth system spec
def password(value):
    if len(value) < 6:
        raise ValueError('password too short, length must be greater than 6')

    if value.count(' ') > 0:
        raise ValueError('password must not contain space(s)')

    return value
