from webargs import fields

from ..api.validators import Email, password

user_args = {
    'email': fields.Str(validate=Email, required=True),
    'password': fields.Str(validate=password, required=True)
}

role_args = {
    'name': fields.Str(required=True),
    'description': fields.Str(required=True)
}
