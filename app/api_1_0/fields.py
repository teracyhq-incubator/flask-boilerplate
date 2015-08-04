from flask_restful import fields

from ..api.fields import iso8601_datetime

paging_fields = {
    'count': fields.Integer,
    'offset': fields.Integer,
    'limit': fields.Integer,
    'previous': fields.String,
    'next': fields.String,
}


user_fields = {
    'id': fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String,
    'full_name': fields.String,
    'email': fields.String,
    'public_name': fields.String,
    'logo_image_name': fields.String,
    'active': fields.Boolean,
    'status': fields.String,
    'is_subscribed': fields.Boolean,
    'date_created': iso8601_datetime,
    'is_deleted': fields.String,
    'date_modified': iso8601_datetime,
    'confirmed_at': iso8601_datetime,
    'is_premium': fields.Boolean
}

user_token_fields = {
    'user': fields.Nested(user_fields),
    'token': fields.String
}


user_list_fields = {
    'data': fields.List(fields.Nested(user_fields)),
    'paging': fields.Nested(paging_fields)
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
