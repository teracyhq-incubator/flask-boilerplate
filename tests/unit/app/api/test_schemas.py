

from tests.unit import UnitTestCase

from app.api.schemas import Schema
from marshmallow import fields


class SchemasTestCase(UnitTestCase):

    def test_fields_to_dict(self):
        from app.api.schemas import fields_to_dict

        self.assertEqual({}, fields_to_dict(None))
        self.assertEqual({}, fields_to_dict(''))

        _fields = 'id,name'
        result = fields_to_dict(_fields)

        expected = {
            'id': {},
            'name': {}
        }

        self.assertEqual(result, expected)

        _fields = 'id,name,roles{id,name,description}'
        expected = {
            'id': {},
            'name': {},
            'roles': {
                'id': {},
                'name': {},
                'description': {}
            }
        }

        result = fields_to_dict(_fields)

        self.assertEqual(result, expected)

        _fields = 'id,name,roles[0:5]{id,name,description}'

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

        self.assertEqual(fields_to_dict(_fields), expected)

        _fields = 'id,name,roles[0:5]{id,name,description},' +\
                    'A{12{A1,A2},34{A3,A4[300:400]},56{A7{A8{}}}}'

        expected = {
            'id': {},
            'name': {},
            'roles': {
                '__slice': '0:5',
                'id': {},
                'name': {},
                'description': {}
            },
            'A': {
                '12': {
                    'A1': {},
                    'A2': {}
                },
                '34': {
                    'A3': {},
                    'A4': {
                        '__slice': '300:400',
                    }
                },
                '56': {
                    'A7': {
                        'A8': {}
                    }
                }
            }
        }

        self.assertEqual(fields_to_dict(_fields), expected)

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
        self.assertEqual(result.get('roles')[0].get('description'), None)
        self.assertEqual(result.get('roles')[1].get('description'), None)

    def test_filter_list(self):
        from app.api.schemas import filter_list

        origin_list = [{
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
        }, {
            'id': 2,
            'email': 'test2@example.com',
            'active': False,
        }]

        self.assertEqual(filter_list(origin_list), origin_list)

        result = filter_list(origin_list, fields='id,email')

        self.assertEqual(len(result[0]), 2)
        self.assertEqual(len(result[1]), 2)
        self.assertEqual(result[0].get('id'), 1)
        self.assertEqual(result[1].get('id'), 2)

        result = filter_list(origin_list, fields='id,email,active,roles{id,name}')

        self.assertEqual(len(result[0]), 4)
        self.assertEqual(len(result[1]), 3)
        self.assertEqual(len(result[0].get('roles')), 2)
        self.assertEqual(result[1].get('roles'), None)

    def test_dump(self):

        class SampleSchema(Schema):
            id = fields.Int()
            email = fields.Email()
            active = fields.Bool()

        sample_schema = SampleSchema()
        sample_obj = {
            'id': 1,
            'email': 'test@example.com',
            'active': True,
        }

        # No fields
        result, errors = sample_schema.dump(sample_obj, fields=None)

        self.assertEqual(len(result), 3)

        # With fields
        result, errors = sample_schema.dump(sample_obj, fields='id, email')

        self.assertEqual(len(result), 2)
        self.assertEqual(result.get('id'), 1)
        self.assertEqual(result.get('email'), 'test@example.com')

        # With many=True
        sample_obj_list = [{
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
        }, {
            'id': 2,
            'email': 'test2@example.com',
            'active': False,
        }]

        result, errors = sample_schema.dump(sample_obj_list, fields='id', many=True)

        self.assertEqual(len(result), 2)
        self.assertEqual(type(result), type(sample_obj_list))
        self.assertEqual(len(result[0]), 1)
        self.assertEqual(result[0].get('id'), sample_obj_list[0].get('id'))

    def test_dumps(self):
        import json

        class SampleSchema(Schema):
            id = fields.Int()
            email = fields.Email()
            active = fields.Bool()

        class SampleRoleSchema(Schema):
            id = fields.Int()
            name = fields.Str()
            description = fields.Str()

        class SampleRolesSchema(Schema):
            id = fields.Int()
            email = fields.Email()
            active = fields.Bool()
            roles = fields.List(fields.Nested(SampleRoleSchema))

        sample_schema = SampleSchema()
        sample_obj = {
            'id': 1,
            'email': 'test@example.com',
            'active': True,
        }

        # No fields
        result, errors = sample_schema.dumps(sample_obj, fields=None)

        self.assertEqual(type(result), str)
        self.assertEqual(result, json.dumps(sample_obj))

        # With fields
        result, errors = sample_schema.dumps(sample_obj, fields='id, email')

        desired_obj = {
            'id': 1,
            'email': 'test@example.com',
        }
        self.assertEqual(result, json.dumps(desired_obj))

        # With many=True
        sample_obj_list = [{
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
        }, {
            'id': 2,
            'email': 'test2@example.com',
            'active': False,
        }]

        desired_obj_list = [{
            'id': 1,
            'roles': [{
                'id': 1,
                'name': 'user',
            }, {
                'id': 2,
                'name': 'admin',
            }]
        }, {
            'id': 2,
            'roles': []
        }]

        sample_role_schema = SampleRolesSchema()

        result, errors = sample_role_schema.dumps(sample_obj_list, fields='id,roles{id,name}', many=True)

        self.assertEqual(result, json.dumps(desired_obj_list))
        self.assertEqual(type(result), str)

        # result have sliced on return

        sample_obj_list = [{
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
            }, {
                'id': 3,
                'name': 'admin2',
                'description': 'admin role'
            }, {
                'id': 4,
                'name': 'admin3',
                'description': 'admin role'
            }]
        }, {
            'id': 2,
            'email': 'test2@example.com',
            'active': False,
        }]

        desired_obj_list = [{
            'id': 1,
            'roles': [{
                'id': 2,
                'name': 'admin',
            }, {
                'id': 3,
                'name': 'admin2',
            }]
        }, {
            'id': 2,
            'roles': []
        }]

        result, errors = sample_role_schema.dumps(sample_obj_list, fields='id,roles[1:3]{id,name}',
                                                  many=True)

        self.assertEqual(result, json.dumps(desired_obj_list))
        self.assertEqual(type(result), str)
