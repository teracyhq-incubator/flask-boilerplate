# -*- coding: utf-8 -*-

"""Roles API"""

from flask import url_for
from flask_restful import marshal_with

from ..extensions import auth_datastore
from ..api import (TokenRequiredResource, AdminRoleRequiredResource, permissions_required,
                   paginated, make_empty_response, marshal_with_data_envelope)
from ..auth import admin_role_permission
from . import api
from .fields import role_fields, role_list_fields


@api.resource('/roles', endpoint='roles')
class RoleListAPI(AdminRoleRequiredResource):

    def __init__(self):
        # TODO(hoatle): have init_action_method to init arguments instead?
        # for example: init_get, init_post, init_update, init_delete?
        # because super() here must always called first, could cause some problems when it's not
        # called first
        super(RoleListAPI, self).__init__()

        self.add_argument('get', 'name', str, help='role name')
        self.add_argument('get', 'description', str, help='role description')

        self.add_argument('post', 'name', str, required=True, help='role name')
        self.add_argument('post', 'description', str, required=True, help='role description')

    @marshal_with(role_list_fields)
    @paginated
    def get(self):
        args = self.parse_arguments()
        return auth_datastore.find_roles(**args), args

    @marshal_with_data_envelope(role_fields)
    def post(self):
        role = auth_datastore.create_role(**self.parse_arguments())
        location = url_for('.role', **{'role_id': role.id})
        return role, 201, {
            'Location': location
        }


@api.resource('/roles/<int:role_id>', endpoint='role')
class RoleAPI(TokenRequiredResource):

    action_decorators = {
        'put': [permissions_required(admin_role_permission)],
        'delete': [permissions_required(admin_role_permission)]
    }

    def __init__(self):
        super(RoleAPI, self).__init__()
        self.add_argument('put', 'name', str, required=True, help='role name')
        self.add_argument('put', 'description', str, required=True, help='role description')

    @marshal_with_data_envelope(role_fields)
    def get(self, role_id):
        return auth_datastore.read_role(role_id, **self.parse_arguments())

    @marshal_with_data_envelope(role_fields)
    def put(self, role_id):
        return auth_datastore.update_role(role_id, **self.parse_arguments())

    def delete(self, role_id):
        auth_datastore.delete_role(role_id, **self.parse_arguments())
        return make_empty_response(200)
