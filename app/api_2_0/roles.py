from flask import url_for
from flask_classy import route
from webargs import Arg
from webargs.flaskparser import use_args

from ..api import permissions_required, token_auth_required, paginated
from ..auth.permissions import admin_role_permission
from ..extensions import auth_datastore

from .base import Resource, marshal_with
from .schemas import RoleSchema, RoleListSchema
from .args import role_args

_role_schema = RoleSchema()

search_args = {
    'name': Arg(str),
    'description': Arg(str)
}


class RoleAPI(Resource):

    decorators = [token_auth_required()]

    @route('', methods=['GET'])
    @permissions_required(admin_role_permission)
    @marshal_with(RoleListSchema())
    @paginated
    @use_args(search_args)
    def index(self, args):
        return auth_datastore.find_roles(**args), args

    @marshal_with(_role_schema, envelope='data')
    def show(self, id):
        return auth_datastore.read_role(id)

    @route('', methods=['POST'])
    @permissions_required(admin_role_permission)
    @marshal_with(_role_schema, envelope='data')
    @use_args(role_args)
    def create(self, args):
        role = auth_datastore.create_role(**args)
        location = url_for('.roles.show', _external=True, **{'id': role.id})
        return role, 201, {
            'Location': location
        }

    @route('<id>', methods=['PUT'])
    @permissions_required(admin_role_permission)
    @marshal_with(_role_schema, envelope='data')
    @use_args(search_args)
    def update(self, args, id):
        return auth_datastore.update_role(id, **args)

    @permissions_required(admin_role_permission)
    def destroy(self, id):
        auth_datastore.delete_role(id)
        return ''
