from typing import Optional
from api.common.utils import get_utc_now, get_logger, validate_uuid

from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from api.common.base_repository import BaseRepository
from api.domain.entities.user_password_reset import UserPasswordReset

logger = get_logger(__name__)


class UserPasswordResetRepository(BaseRepository[UserPasswordReset]):
    def __init__(self, session: AsyncSession):
        super().__init__(UserPasswordReset, session)

    async def set_password_reset(
        self, user_id: str, first_name: str, tenant_id: str | None = None
    ) -> UserPasswordReset:
        """设置用户密码重置"""
        try:
            validated_user_id = validate_uuid(user_id, "User ID")
            validated_tenant_id = (
                validate_uuid(tenant_id, "Tenant ID") if tenant_id else None
            )

            existing = await self.single_or_none(user_id=validated_user_id)
            token_secret = uuid4()

            if existing:
                updated_data = {
                    "token_secret": str(token_secret),
                    "reset_secret_updated_at": get_utc_now(),
                }
                logger.info(f"Updating password reset for user {user_id}")
                return await self.update(existing.id, updated_data)

            reset_data = {
                "user_id": validated_user_id,
                "token_secret": str(token_secret),
                "reset_secret_updated_at": get_utc_now(),
                "tenant_id": validated_tenant_id,
                "first_name": first_name,
            }
            logger.info(f"Creating password reset for user {user_id}")
            return await super().create(reset_data)
        except ValueError:
            logger.error(
                f"Invalid UUID format for user_id: {user_id} or tenant_id: {tenant_id}"
            )
            raise

    async def get_by_token_secret(
        self, token_secret: str
    ) -> Optional[UserPasswordReset]:
        """根据 token_secret 获取密码重置记录"""
        return await self.single_or_none(token_secret=token_secret)

    async def delete_by_user_id(self, user_id: str) -> bool:
        """根据用户 ID 删除密码重置记录"""
        try:
            validated_user_id = validate_uuid(user_id, "User ID")
            existing = await self.single_or_none(user_id=validated_user_id)
            if existing is None:
                logger.warning(f"Password reset not found for user {user_id}")
                return False
            await self.delete(existing.id)
            logger.info(f"Deleted password reset for user {user_id}")
            return True
        except ValueError:
            logger.error(f"Invalid UUID format for user_id: {user_id}")
            return False
