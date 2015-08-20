# -*- coding: utf-8 -*-

"""app.api_1_0 tests"""

from mock import patch
from tests.unit import UnitTestCase


class AuthTestCase(UnitTestCase):

    @patch('app.api_1_0.g')
    def test_before_request(self, mock_g):
        from app.api_1_0 import before_request

        before_request()

        self.assertIsNone(mock_g.token_auth_used)
        self.assertIsNone(mock_g.http_auth_used)
