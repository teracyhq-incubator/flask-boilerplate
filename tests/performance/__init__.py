"""performance tests"""

import unittest

from nose.plugins.attrib import attr


@attr('perf')
class PerformanceTestCase(unittest.TestCase):
    """Base PerformanceTestCase"""
    pass
