from api.common.base_repository import BaseRepository
from api.domain.entities.ai import ChatSessionAI
from sqlalchemy.ext.asyncio import AsyncSession


class ChatSessionAIRepository(BaseRepository[ChatSessionAI]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(ChatSessionAI, session)

    async def is_session_exists(self, session_id: str) -> bool:
        """检查会话是否存在"""
        existing = await self.single_or_none(session_id=session_id)
        return existing is not None
