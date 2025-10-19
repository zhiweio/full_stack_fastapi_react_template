"""
简化的全局依赖注入容器
支持在非 FastAPI 路由函数中获取服务实例
"""

from typing import Optional, Dict, Any
from contextlib import asynccontextmanager
from functools import lru_cache


class DependencyContainer:
    """简化的依赖注入容器"""

    def __init__(self):
        self._instances: Dict[str, Any] = {}

    @asynccontextmanager
    async def get_session(self):
        """获取数据库会话的上下文管理器"""
        # 延迟导入避免循环依赖
        from api.infrastructure.persistence.database import get_db_session

        async with get_db_session() as session:
            yield session

    async def get_tenant_service(self):
        """获取租户服务实例"""
        # 延迟导入避免循环依赖
        from api.infrastructure.persistence.repositories.tenant_repository_impl import (
            TenantRepository,
        )
        from api.usecases.tenant_service import TenantService

        async with self.get_session() as session:
            tenant_repo = TenantRepository(session)
            return TenantService(tenant_repo)

    async def get_user_service(self):
        """获取用户服务实例"""
        # 延迟导入避免循环依赖
        from api.infrastructure.persistence.repositories.user_repository_impl import (
            UserRepository,
        )
        from api.infrastructure.persistence.repositories.user_password_reset_repository_impl import (
            UserPasswordResetRepository,
        )
        from api.usecases.user_service import UserService

        async with self.get_session() as session:
            user_repo = UserRepository(session)
            user_password_reset_repo = UserPasswordResetRepository(session)
            return UserService(user_repo, user_password_reset_repo)

    async def get_role_service(self):
        """获取角色服务实例"""
        # 延迟导入避免循环依赖
        from api.infrastructure.persistence.repositories.role_repository_impl import (
            RoleRepository,
        )
        from api.usecases.role_service import RoleService

        async with self.get_session() as session:
            role_repo = RoleRepository(session)
            return RoleService(role_repo)

    async def get_auth_service(self):
        """获取认证服务实例"""
        # 延迟导入避免循环依赖
        from api.infrastructure.persistence.repositories.user_repository_impl import (
            UserRepository,
        )
        from api.infrastructure.persistence.repositories.role_repository_impl import (
            RoleRepository,
        )
        from api.usecases.user_service import UserService
        from api.usecases.auth_service import AuthService

        async with self.get_session() as session:
            user_repo = UserRepository(session)
            role_repo = RoleRepository(session)
            user_service = UserService(user_repo, role_repo)
            return AuthService(user_service)

    def clear_instances(self):
        """清除缓存的实例"""
        self._instances.clear()


# 全局容器实例
@lru_cache()
def get_container() -> DependencyContainer:
    """获取全局依赖注入容器实例"""
    return DependencyContainer()
