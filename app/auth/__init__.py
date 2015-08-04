# -*- coding: utf-8 -*-

"""auth extension"""

from .decorators import permissions_required, permissions_accepted, roles_required, roles_accepted
from .permissions import user_role_permission, admin_role_permission, user_permission
