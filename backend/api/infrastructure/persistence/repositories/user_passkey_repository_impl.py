from typing import Literal, Optional
from uuid import UUID
import base64

from api.common.base_repository import BaseRepository
from api.common.utils import get_logger
from api.domain.entities.user_passkey import Challenges, UserPasskey

logger = get_logger(__name__)


class UserPasskeyRepository(BaseRepository[UserPasskey]):
    def __init__(self):
        super().__init__(UserPasskey)

    async def get_by_user_email(self, user_email: str) -> Optional[UserPasskey]:
        """根据用户邮箱获取 Passkey"""
        return await self.single_or_none(user_email=user_email)


class UserPasskeyChallengesRepository(BaseRepository[Challenges]):
    def __init__(self):
        super().__init__(Challenges)

    async def save_challenge(
        self,
        email: str,
        challenge: bytes,
        type: Literal["registration", "authentication"],
        tenant_id: Optional[UUID] = None,
    ) -> Challenges:
        """
        Save challenges with current user email, return challenge
        """
        cv = base64.urlsafe_b64encode(challenge).decode("utf-8").rstrip("=")
        logger.debug(f"challenge bytes to a string {cv}")

        challenge_data = {
            "email": email,
            "challenge": cv,
            "type": type,
            "tenant_id": tenant_id,
        }
        return await super().create(challenge_data)

    async def get_challenge(
        self, email: str, type: Literal["registration", "authentication"]
    ) -> Optional[Challenges]:
        """
        Returns current challenge for the given email if found otherwise, None
        """
        return await self.single_or_none(email=email, type=type)

    async def delete_challenge(
        self, email: str, type: Literal["registration", "authentication"]
    ) -> bool:
        """
        Delete the current challenge for the given email, Returns False if its not found, Otherwise, True
        """
        existing = await self.get_challenge(email=email, type=type)
        if existing is None:
            return False
        await self.delete(existing.id)
        return True
