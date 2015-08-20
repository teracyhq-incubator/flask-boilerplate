import json

from tests.integration import IntegrationTestCase


class RoleResourceTestCase(IntegrationTestCase):

    def test_index_invalid_auth(self):
        rv = self.client.get('/api/v1.0/roles')
        self.assertEqual(rv.status_code, 401)
        resp = json.loads(rv.data)
        error = resp.get('error')
        self.assertEqual(error.get('message'), 'Authorization Required')
        self.assertEqual(error.get('description'), 'Authorization header was missing')

    def test_index_invalid_perm(self):
        pass

    def test_index_valid_perm(self):
        pass

    def test_create_invalid_auth(self):
        rv = self.client.post('/api/v1.0/roles')
        self.assertEqual(rv.status_code, 401)
        resp = json.loads(rv.data)
        error = resp.get('error')
        self.assertEqual(error.get('message'), 'Authorization Required')
        self.assertEqual(error.get('description'), 'Authorization header was missing')

    def test_create_invalid_perm(self):
        pass

    def test_create_valid_perm(self):
        pass


    def test_show_invalid_auth(self):
        rv = self.client.get('/api/v1.0/roles/1')
        self.assertEqual(rv.status_code, 401)
        resp = json.loads(rv.data)
        error = resp.get('error')
        self.assertEqual(error.get('message'), 'Authorization Required')
        self.assertEqual(error.get('description'), 'Authorization header was missing')

    def test_show_invalid_perm(self):
        pass

    def test_show_valid_perm(self):
        pass

    def test_update_invalid_auth(self):
        rv = self.client.put('/api/v1.0/roles/1')
        self.assertEqual(rv.status_code, 401)
        resp = json.loads(rv.data)
        error = resp.get('error')
        self.assertEqual(error.get('message'), 'Authorization Required')
        self.assertEqual(error.get('description'), 'Authorization header was missing')

    def test_update_invalid_perm(self):
        pass

    def test_update_valid_perm(self):
        pass

    def test_destroy_invalid_auth(self):
        rv = self.client.delete('/api/v1.0/roles/1')
        self.assertEqual(rv.status_code, 401)
        resp = json.loads(rv.data)
        error = resp.get('error')
        self.assertEqual(error.get('message'), 'Authorization Required')
        self.assertEqual(error.get('description'), 'Authorization header was missing')

    def test_destroy_invalid_perm(self):
        pass

    def test_destroy_valid_perm(self):
        pass
