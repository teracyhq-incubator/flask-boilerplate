from flask import url_for
from flask_classy import route
from webargs import fields
from webargs.flaskparser import use_args

from ..api import (TokenRequiredResource, marshal_with, marshal_with_data_envelope,
                   permissions_required, paginated, make_empty_response)
from ..api.decorators import extract_args
from ..auth.permissions import admin_role_permission
from ..extensions import auth_datastore

from .schemas import RoleSchema, RoleListSchema
from .args import role_args

_role_schema = RoleSchema()

search_args = {
    'name': fields.Str(),
    'description': fields.Str()
}


class RoleResource(TokenRequiredResource):

    @route('', methods=['GET'])
    @permissions_required(admin_role_permission)
    @marshal_with(RoleListSchema())
    @paginated
    @extract_args(search_args)
    def list(self, args):
        return auth_datastore.find_roles(**args), args

    @marshal_with_data_envelope(_role_schema)
    def read(self, id):
        return auth_datastore.read_role(id)

    @route('', methods=['POST'])
    @permissions_required(admin_role_permission)
    @marshal_with_data_envelope(_role_schema)
    @use_args(role_args)
    def create(self, args):
        role = auth_datastore.create_role(**args)
        location = url_for('.roles.read', _external=True, **{'id': role.id})
        return role, 201, {
            'Location': location
        }

    @route('<id>', methods=['PUT'])
    @permissions_required(admin_role_permission)
    @marshal_with_data_envelope(_role_schema)
    @use_args(search_args)
    def update(self, args, id):
        return auth_datastore.update_role(id, **args)

    @permissions_required(admin_role_permission)
    def delete(self, id):
        auth_datastore.delete_role(id)
        return make_empty_response(200)
