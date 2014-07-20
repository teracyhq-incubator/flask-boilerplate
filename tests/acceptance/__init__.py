"""acceptance tests"""

import unittest

from nose.plugins.attrib import attr


@attr('acc')
class AcceptanceTestCase(unittest.TestCase):
    """Base AcceptanceTestCase"""
    pass
