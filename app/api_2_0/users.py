from flask import url_for
from flask_security import current_user
from flask_classy import route, FlaskView
from webargs import Arg
from webargs.flaskparser import use_args

from ..auth import admin_role_permission, user_permission
from ..api import (token_auth_required, one_of, anonymous_required, permissions_required,
                   validators, paginated)
from ..extensions import auth_datastore
from ..exceptions import UnauthorizedException

from .base import Resource, marshal_with
from .schemas import UserSchema, UserListSchema
from .args import user_args

_user_schema = UserSchema()

search_args = {
    'email': Arg(str, validate=validators.Email()),
    'active': Arg(bool)  # TODO(hoatle): add boolean validator here
}


class UserAPI(Resource):

    @staticmethod
    def _check_current_user_or_admin_role(user_id):
        if 'me' == user_id:
            user_id = current_user.id

        specified_user_permission = user_permission(long(user_id))

        if not (specified_user_permission.can() or admin_role_permission.can()):
            description = '{} or {} required'.format(specified_user_permission,
                                                     admin_role_permission)
            raise UnauthorizedException('Invalid Permission',
                                        description=description)
        return user_id

    @route('', methods=['GET'])
    @token_auth_required()
    @permissions_required(admin_role_permission)
    @marshal_with(UserListSchema())
    @paginated
    @use_args(search_args)
    def index(self, args):
        return auth_datastore.find_users(**args), args


    @token_auth_required()
    @marshal_with(_user_schema, envelope='data')
    def show(self, id):
        id = self._check_current_user_or_admin_role(id)
        user = auth_datastore.read_user(id)
        return user

    @route('', methods=['POST'])
    @one_of(anonymous_required, permissions_required(admin_role_permission))
    @marshal_with(_user_schema, envelope='data')
    @use_args(user_args)
    def create(self, args):
        user = auth_datastore.create_user(**args)
        location = url_for('.users:show', _external=True, **{'id': user.id})
        return user, 201, {
            'Location': location
        }

    @route('<id>', methods=['PUT'])
    @marshal_with(_user_schema, envelope='data')
    @use_args({
        'email': Arg(str, validate=validators.Email()),
        'active': Arg(bool)
    })
    def update(self, args, id):
        id = self._check_current_user_or_admin_role(id)
        return auth_datastore.update_user(id, **args)

    @permissions_required(admin_role_permission)
    def destroy(self, id):
        auth_datastore.delete_user(id)
        return ''
