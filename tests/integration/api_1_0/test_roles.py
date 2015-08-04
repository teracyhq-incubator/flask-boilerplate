import json

from tests.integration import IntegrationTestCase


class RoleListAPITestCase(IntegrationTestCase):

    def test_get_invalid_auth(self):
        rv = self.client.get('/api/v1.0/roles')
        self.assertEqual(rv.status_code, 401)
        resp = json.loads(rv.data)
        error = resp.get('error')
        self.assertEqual(error.get('message'), 'Authorization Required')
        self.assertEqual(error.get('description'), 'Authorization header was missing')

    def test_get_invalid_perm(self):
        pass

    def test_get_valid_perm(self):
        pass

    def test_post_invalid_auth(self):
        rv = self.client.post('/api/v1.0/roles')
        self.assertEqual(rv.status_code, 401)
        resp = json.loads(rv.data)
        error = resp.get('error')
        self.assertEqual(error.get('message'), 'Authorization Required')
        self.assertEqual(error.get('description'), 'Authorization header was missing')

    def test_post_invalid_perm(self):
        pass

    def test_post_valid_perm(self):
        pass


class RoleAPITestCase(IntegrationTestCase):

    def test_get_invalid_auth(self):
        rv = self.client.get('/api/v1.0/roles/1')
        self.assertEqual(rv.status_code, 401)
        resp = json.loads(rv.data)
        error = resp.get('error')
        self.assertEqual(error.get('message'), 'Authorization Required')
        self.assertEqual(error.get('description'), 'Authorization header was missing')

    def test_get_invalid_perm(self):
        pass

    def test_get_valid_perm(self):
        pass

    def test_put_invalid_auth(self):
        rv = self.client.put('/api/v1.0/roles/1')
        self.assertEqual(rv.status_code, 401)
        resp = json.loads(rv.data)
        error = resp.get('error')
        self.assertEqual(error.get('message'), 'Authorization Required')
        self.assertEqual(error.get('description'), 'Authorization header was missing')

    def test_put_invalid_perm(self):
        pass

    def test_put_valid_perm(self):
        pass

    def test_delete_invalid_auth(self):
        rv = self.client.delete('/api/v1.0/roles/1')
        self.assertEqual(rv.status_code, 401)
        resp = json.loads(rv.data)
        error = resp.get('error')
        self.assertEqual(error.get('message'), 'Authorization Required')
        self.assertEqual(error.get('description'), 'Authorization header was missing')

    def test_delete_invalid_perm(self):
        pass

    def test_delete_valid_perm(self):
        pass
