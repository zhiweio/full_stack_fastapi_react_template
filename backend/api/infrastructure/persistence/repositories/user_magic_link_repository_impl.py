from typing import Optional
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from api.common.utils import get_logger, validate_uuid, get_utc_now
from datetime import datetime

from api.common.base_repository import BaseRepository
from api.common.exceptions import ApiBaseException
from api.domain.entities.user_magic_link import UserMagicLink

logger = get_logger(__name__)


class UserMagicLinkRepository(BaseRepository[UserMagicLink]):
    def __init__(self, session: AsyncSession):
        super().__init__(UserMagicLink, session)

    async def create_magic_link(self, user_id: str, token: str) -> UserMagicLink:
        """
        Create a magic link for the given user ID with the provided token.
        Raises an exception if the user has exceeded the allowed number of magic link requests.
        Args:
            user_id (str): The ID of the user to create the magic link for.
            token (str): The token to associate with the magic link.
        Returns:
            UserMagicLink: The created UserMagicLink document.
        """
        try:
            validated_user_id = validate_uuid(user_id, "User ID")
            count = await self.count(user_id=validated_user_id)
            logger.info(f"Magic link requests count for user {user_id}: {count}")
            if count > 3:
                raise ApiBaseException(
                    "Too many magic link requests. Please try again later."
                )

            magic_link_data = {"user_id": validated_user_id, "token": token}
            return await super().create(magic_link_data)
        except ValueError:
            logger.error(f"Invalid UUID format for user_id: {user_id}")
            raise ApiBaseException("Invalid user ID format")

    async def get_by_token(self, token: str) -> Optional[UserMagicLink]:
        """根据 token 获取魔法链接"""
        return await self.single_or_none(token=token)

    async def delete_expired_links(self) -> int:
        """删除过期的魔法链接"""
        session = await self.get_session()
        from sqlmodel import select, delete

        # 查找过期的链接
        now = get_utc_now()
        expired_statement = select(UserMagicLink).where(UserMagicLink.expires_at < now)
        expired_result = await session.exec(expired_statement)
        expired_links = expired_result.all()

        if expired_links:
            # 删除过期的链接
            delete_statement = delete(UserMagicLink).where(
                UserMagicLink.expires_at < now
            )
            await session.exec(delete_statement)
            await session.commit()

        return len(expired_links)
