"""integration tests"""

import unittest

from nose.plugins.attrib import attr


@attr('intg')
class IntegrationTestCase(unittest.TestCase):
    """Base IntegrationTestCase"""
    pass
