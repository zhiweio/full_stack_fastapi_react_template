# Factory methods for common permission patterns
from typing import List
from fastapi import Depends
from api.domain.enum.permission import Permission
from api.domain.security.user_access_management import UserAccessManagement
from api.core.dependencies import get_role_service, RoleServiceDep


def check_permissions_for_current_role(
    required_permissions: List[Permission],
    any_permission: bool = False,
    allow_self_access: bool = False,
):
    """Returns a dependency function that checks permissions for the current role."""

    def dependency(role_service: RoleServiceDep):
        return UserAccessManagement(
            required_permissions=required_permissions,
            any_permission=any_permission,
            allow_self_access=allow_self_access,
        )(role_service)

    return dependency
