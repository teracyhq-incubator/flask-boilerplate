

from tests.unit import UnitTestCase


class SchemasTestCase(UnitTestCase):

    def test_fields_to_dict(self):
        from app.api.schemas import fields_to_dict

        self.assertEqual({}, fields_to_dict(None))
        self.assertEqual({}, fields_to_dict(''))

        fields = 'id,name'
        result = fields_to_dict(fields)

        expected = {
            'id': {},
            'name': {}
        }

        self.assertEqual(result, expected)

        fields = 'id,name,roles{id,name,description}'
        expected = {
            'id': {},
            'name': {},
            'roles': {
                'id': {},
                'name': {},
                'description': {}
            }
        }

        result = fields_to_dict(fields)

        self.assertEqual(result, expected)

        fields = 'id,name,roles[0:5]{id,name,description}'

        expected = {
            'id': {},
            'name': {},
            'roles': {
                '__slice': '0:5',
                'id': {},
                'name': {},
                'description': {}
            }
        }

        self.assertEqual(fields_to_dict(fields), expected)

    def test_filter_dict(self):

        from app.api.schemas import filter_dict

        origin_dict = {
            'id': 1,
            'email': 'test@example.com',
            'active': True,
            'roles': [{
                'id': 1,
                'name': 'user',
                'description': 'user role'
            }, {
                'id': 2,
                'name': 'admin',
                'description': 'admin role'
            }]
        }

        self.assertEqual(filter_dict(origin_dict), origin_dict)

        result = filter_dict(origin_dict, fields='id,email')

        self.assertEqual(len(result), 2)
        self.assertEqual(result.get('id'), 1)
        self.assertEqual(result.get('email'), 'test@example.com')

        result = filter_dict(origin_dict, fields='id,email,active,roles{id,name}')

        self.assertEqual(len(result), 4)
