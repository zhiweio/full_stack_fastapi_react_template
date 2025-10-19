from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.common.base_repository import BaseRepository
from api.domain.entities.role import Role
from api.domain.entities.storage_settings import StorageSettings
from api.domain.entities.tenant import Tenant
from api.domain.entities.user import User
from api.domain.entities.user_magic_link import UserMagicLink
from api.infrastructure.persistence.database import get_db_session
from api.infrastructure.persistence.repositories.role_repository_impl import (
    RoleRepository,
)
from api.infrastructure.persistence.repositories.storage_settings_repository_impl import (
    StorageSettingsRepository,
)
from api.infrastructure.persistence.repositories.tenant_repository_impl import (
    TenantRepository,
)
from api.infrastructure.persistence.repositories.user_magic_link_repository_impl import (
    UserMagicLinkRepository,
)
from api.infrastructure.persistence.repositories.user_repository_impl import (
    UserRepository,
)
from api.infrastructure.persistence.repositories.user_preference_repository_impl import (
    UserPreferenceRepository,
)
from api.infrastructure.persistence.repositories.chat_session_ai_repository_impl import (
    ChatSessionAIRepository,
)
from api.infrastructure.persistence.repositories.chat_history_ai_repository_impl import (
    ChatHistoryAIRepository,
)
from api.infrastructure.persistence.repositories.user_password_reset_repository_impl import (
    UserPasswordResetRepository,
)
from api.infrastructure.persistence.repositories.user_passkey_repository_impl import (
    UserPasskeyRepository,
    UserPasskeyChallengesRepository,
)
from api.usecases.auth_service import AuthService
from api.usecases.local_ai_service import LocalAIService
from api.usecases.file_service import FileService
from api.usecases.role_service import RoleService
from api.usecases.tenant_service import TenantService
from api.usecases.user_service import UserService
from api.usecases.user_preference_service import UserPreferenceService
from api.usecases.storage_settings_service import StorageSettingsService
from api.usecases.coolify_app_service import CoolifyAppService
from api.usecases.magic_link_service import EmailMagicLinkService
from api.infrastructure.security.jwt_token_service import JwtTokenService
from api.domain.interfaces.email_service import IEmailService
from api.infrastructure.externals.coolify_app import CoolifyApp
from api.infrastructure.security.passkey_service import PasskeyService
from api.infrastructure.externals.dns_resolver import DnsResolver


# Repository dependencies
async def get_user_repository(
    session: Annotated[BaseRepository, Depends(get_db_session)],
) -> UserRepository:
    """获取用户仓储实例"""
    return UserRepository(session)


async def get_role_repository(
    session: Annotated[BaseRepository, Depends(get_db_session)],
) -> RoleRepository:
    """获取角色仓储实例"""
    return RoleRepository(session)


async def get_tenant_repository(
    session: Annotated[BaseRepository, Depends(get_db_session)],
) -> TenantRepository:
    """获取租户仓储实例"""
    return TenantRepository(session)


async def get_storage_settings_repository(
    session: Annotated[BaseRepository, Depends(get_db_session)],
) -> StorageSettingsRepository:
    """获取存储设置仓储实例"""
    return StorageSettingsRepository(session)


async def get_user_magic_link_repository(
    session: Annotated[BaseRepository, Depends(get_db_session)],
) -> UserMagicLinkRepository:
    """获取用户魔法链接仓储实例"""
    return UserMagicLinkRepository(session)


async def get_user_preference_repository(
    session: Annotated[BaseRepository, Depends(get_db_session)],
) -> UserPreferenceRepository:
    """获取用户偏好仓储实例"""
    return UserPreferenceRepository(session)


async def get_chat_session_ai_repository(
    session: Annotated[BaseRepository, Depends(get_db_session)],
) -> ChatSessionAIRepository:
    """获取聊天会话AI仓储实例"""
    return ChatSessionAIRepository(session)


async def get_chat_history_ai_repository(
    session: Annotated[BaseRepository, Depends(get_db_session)],
) -> ChatHistoryAIRepository:
    """获取聊天历史AI仓储实例"""
    return ChatHistoryAIRepository(session)


async def get_user_password_reset_repository(
    session: Annotated[BaseRepository, Depends(get_db_session)],
) -> UserPasswordResetRepository:
    """获取用户密码重置仓储实例"""
    return UserPasswordResetRepository(session)


# Service dependencies
def get_jwt_token_service() -> JwtTokenService:
    """获取JWT令牌服务实例"""
    return JwtTokenService()


def get_email_service() -> IEmailService:
    """获取邮件服务实例"""
    from api.infrastructure.externals.smtp_email import SmtpEmail

    return SmtpEmail()


def get_user_service(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
    user_password_reset_repository: Annotated[
        UserPasswordResetRepository, Depends(get_user_password_reset_repository)
    ],
) -> UserService:
    """获取用户服务实例"""
    return UserService(user_repository, user_password_reset_repository)


def get_role_service(
    role_repository: Annotated[RoleRepository, Depends(get_role_repository)],
) -> RoleService:
    """获取角色服务实例"""
    return RoleService(role_repository)


def get_tenant_service(
    tenant_repository: Annotated[TenantRepository, Depends(get_tenant_repository)],
) -> TenantService:
    """获取租户服务实例"""
    return TenantService(tenant_repository)


def get_auth_service(
    user_service: Annotated[UserService, Depends(get_user_service)],
    tenant_service: Annotated[TenantService, Depends(get_tenant_service)],
    role_service: Annotated[RoleService, Depends(get_role_service)],
    jwt_token_service: Annotated[JwtTokenService, Depends(get_jwt_token_service)],
    email_service: Annotated[IEmailService, Depends(get_email_service)],
) -> AuthService:
    """获取认证服务实例"""
    return AuthService(
        user_service, tenant_service, role_service, jwt_token_service, email_service
    )


def get_file_service() -> FileService:
    """获取文件服务实例"""
    return FileService()


def get_dns_resolver(
    email_service: Annotated[IEmailService, Depends(get_email_service)],
) -> DnsResolver:
    """获取DNS解析器实例"""
    return DnsResolver(email_service)


def get_coolify_app_service() -> CoolifyAppService:
    """获取Coolify应用服务实例"""
    return CoolifyAppService()


def get_coolify_app() -> CoolifyApp:
    """获取Coolify应用实例"""
    return CoolifyApp()


def get_user_passkey_repository(
    session: AsyncSession = Depends(get_db_session),
) -> UserPasskeyRepository:
    return UserPasskeyRepository(session)


def get_user_passkey_challenges_repository(
    session: AsyncSession = Depends(get_db_session),
) -> UserPasskeyChallengesRepository:
    return UserPasskeyChallengesRepository(session)


def get_passkey_service(
    user_passkey_repo: UserPasskeyRepository = Depends(get_user_passkey_repository),
    challenges_repo: UserPasskeyChallengesRepository = Depends(
        get_user_passkey_challenges_repository
    ),
) -> PasskeyService:
    """获取Passkey服务实例"""
    return PasskeyService(user_passkey_repo, challenges_repo)


def get_email_magic_link_service(
    user_magic_link_repository: Annotated[
        UserMagicLinkRepository, Depends(get_user_magic_link_repository)
    ],
    email_service: Annotated[IEmailService, Depends(get_email_service)],
    tenant_service: Annotated[TenantService, Depends(get_tenant_service)],
) -> EmailMagicLinkService:
    """获取邮件魔法链接服务实例"""
    return EmailMagicLinkService(
        user_magic_link_repository=user_magic_link_repository,
        email_service=email_service,
        tenant_service=tenant_service,
    )


def get_user_preference_service(
    user_preference_repository: Annotated[
        UserPreferenceRepository, Depends(get_user_preference_repository)
    ],
) -> UserPreferenceService:
    """获取用户偏好设置服务实例"""
    return UserPreferenceService(user_preference_repository=user_preference_repository)


def get_storage_settings_service(
    storage_settings_repository: Annotated[
        StorageSettingsRepository, Depends(get_storage_settings_repository)
    ],
) -> StorageSettingsService:
    """获取存储设置服务实例"""
    return StorageSettingsService(storage_settings_repository)


def get_local_ai_service(
    chat_session_repository: Annotated[
        ChatSessionAIRepository, Depends(get_chat_session_ai_repository)
    ],
    chat_history_repository: Annotated[
        ChatHistoryAIRepository, Depends(get_chat_history_ai_repository)
    ],
) -> LocalAIService:
    """获取本地AI服务实例"""
    return LocalAIService(chat_session_repository, chat_history_repository)


# Type aliases for dependency injection
UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]
RoleRepositoryDep = Annotated[RoleRepository, Depends(get_role_repository)]
TenantRepositoryDep = Annotated[TenantRepository, Depends(get_tenant_repository)]
StorageSettingsRepositoryDep = Annotated[
    StorageSettingsRepository, Depends(get_storage_settings_repository)
]
UserMagicLinkRepositoryDep = Annotated[
    UserMagicLinkRepository, Depends(get_user_magic_link_repository)
]
UserPreferenceRepositoryDep = Annotated[
    UserPreferenceRepository, Depends(get_user_preference_repository)
]
ChatSessionAIRepositoryDep = Annotated[
    ChatSessionAIRepository, Depends(get_chat_session_ai_repository)
]
ChatHistoryAIRepositoryDep = Annotated[
    ChatHistoryAIRepository, Depends(get_chat_history_ai_repository)
]
UserPasswordResetRepositoryDep = Annotated[
    UserPasswordResetRepository, Depends(get_user_password_reset_repository)
]
UserPasskeyRepositoryDep = Annotated[
    UserPasskeyRepository, Depends(get_user_passkey_repository)
]
UserPasskeyChallengesRepositoryDep = Annotated[
    UserPasskeyChallengesRepository, Depends(get_user_passkey_challenges_repository)
]

UserServiceDep = Annotated[UserService, Depends(get_user_service)]
RoleServiceDep = Annotated[RoleService, Depends(get_role_service)]
TenantServiceDep = Annotated[TenantService, Depends(get_tenant_service)]
AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
FileServiceDep = Annotated[FileService, Depends(get_file_service)]
DnsResolverDep = Annotated[DnsResolver, Depends(get_dns_resolver)]
CoolifyAppServiceDep = Annotated[CoolifyAppService, Depends(get_coolify_app_service)]
CoolifyAppDep = Annotated[CoolifyApp, Depends(get_coolify_app)]
PasskeyServiceDep = Annotated[PasskeyService, Depends(get_passkey_service)]
EmailMagicLinkServiceDep = Annotated[
    EmailMagicLinkService, Depends(get_email_magic_link_service)
]
JwtTokenServiceDep = Annotated[JwtTokenService, Depends(get_jwt_token_service)]
EmailServiceDep = Annotated[IEmailService, Depends(get_email_service)]
UserPreferenceServiceDep = Annotated[
    UserPreferenceService, Depends(get_user_preference_service)
]
StorageSettingsServiceDep = Annotated[
    StorageSettingsService, Depends(get_storage_settings_service)
]
LocalAIServiceDep = Annotated[LocalAIService, Depends(get_local_ai_service)]
