from flask_principal import RoleNeed, UserNeed, Permission


user_role_permission = Permission(RoleNeed('user'))

admin_role_permission = Permission(RoleNeed('admin'))


def user_permission(user_id):
    perm = Permission(UserNeed(user_id))
    user_permission.__repr__ = lambda: perm
    return perm


def role_permission(name):
    perm = Permission(RoleNeed(name))
    role_permission.__repr__ = lambda: perm
    return perm
