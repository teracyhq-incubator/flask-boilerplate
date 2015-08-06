from flask_restful import fields

from ..api.fields import iso8601_datetime

paging_fields = {
    'count': fields.Integer,
    'offset': fields.Integer,
    'limit': fields.Integer,
    'previous': fields.String,
    'next': fields.String,
}

role_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String
}

role_list_fields = {
    'data': fields.List(fields.Nested(role_fields)),
    'paging': fields.Nested(paging_fields)
}


user_fields = {
    'id': fields.Integer,
    'email': fields.String,
    'active': fields.Boolean,
    'confirmed_at': iso8601_datetime,
    'roles': fields.List(fields.Nested(role_fields))
}


user_list_fields = {
    'data': fields.List(fields.Nested(user_fields)),
    'paging': fields.Nested(paging_fields)
}

