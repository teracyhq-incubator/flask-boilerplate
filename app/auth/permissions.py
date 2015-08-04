from flask_principal import RoleNeed, UserNeed, Permission


user_role_permission = Permission(RoleNeed('user'))

admin_role_permission = Permission(RoleNeed('admin'))


def user_permission(user_id, *args, **kwargs):
    return Permission(UserNeed(user_id))
