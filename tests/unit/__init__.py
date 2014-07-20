# -*- coding: utf-8 -*-

"""unit tests"""

import unittest

from nose.plugins.attrib import attr


@attr('unit')
class UnitTestCase(unittest.TestCase):
    """base UnitTestCase"""
    pass
