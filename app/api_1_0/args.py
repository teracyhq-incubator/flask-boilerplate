from webargs import Arg

from ..api.validators import Email, password

user_args = {
    'email': Arg(str, validate=Email, required=True),
    'password': Arg(str, validate=password, required=True)
}

role_args = {
    'name': Arg(str, required=True),
    'description': Arg(str, required=True)
}
