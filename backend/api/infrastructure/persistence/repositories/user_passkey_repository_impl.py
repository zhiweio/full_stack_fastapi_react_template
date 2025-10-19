from typing import Literal, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from api.common.base_repository import BaseRepository
from api.common.utils import get_logger, validate_uuid
from api.domain.entities.user_passkey import UserPasskey, Challenges

logger = get_logger(__name__)


class UserPasskeyRepository(BaseRepository[UserPasskey]):
    def __init__(self, session: AsyncSession):
        super().__init__(UserPasskey, session)

    async def get_by_user_email(self, user_email: str) -> Optional[UserPasskey]:
        return await self.get_by_field("email", user_email)


class UserPasskeyChallengesRepository(BaseRepository[Challenges]):
    def __init__(self, session: AsyncSession):
        super().__init__(Challenges, session)

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
