# -*- coding: utf-8 -*-

"""app.auth.permissions tests"""

from tests.unit import UnitTestCase


class PermissionsTestCase(UnitTestCase):

    def test_user_role_permission(self):

        from app.auth.permissions import user_role_permission, RoleNeed

        self.assertEqual(user_role_permission.needs, {RoleNeed('user')})

    def test_admin_role_permission(self):

        from app.auth.permissions import admin_role_permission, RoleNeed

        self.assertEqual(admin_role_permission.needs, {RoleNeed('admin')})

    def test_user_permission(self):
        from app.auth.permissions import user_permission, UserNeed

        first_user_permission = user_permission(1)

        self.assertEqual(first_user_permission.needs, {UserNeed(1)})
