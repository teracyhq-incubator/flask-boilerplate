import json

from tests.integration import IntegrationTestCase


class ViewsTestCase(IntegrationTestCase):

    def test_hello_world(self):
        rv = self.client.get('/')
        self.assertEqual(rv.status_code, 200)
        self.assertIn('Hello World!', rv.data)

    def test_hello_user(self):
        pass

    def test_api_versions_info(self):
        rv = self.client.get('/api/versions')
        self.assertEqual(rv.status_code, 200)
        expected = {
            "latest": {
                "version": "v1.0",
                "status": "@",
                "info": "developing version, APIs are expected to change and break things"
            },
            "supported": [
                {
                    "version": "v1.0",
                    "status": "@",
                    "info": "developing version, APIs are expected to change and break things"
                }
            ]
        }

        self.assertEqual(json.loads(rv.data), expected)
