from api.common.base_repository import BaseRepository
from api.domain.entities.ai import ChatSessionAI


class ChatSessionAIRepository(BaseRepository[ChatSessionAI]):
    def __init__(self) -> None:
        super().__init__(ChatSessionAI)

    async def is_session_exists(self, session_id: str) -> bool:
        """检查会话是否存在"""
        existing = await self.single_or_none(session_id=session_id)
        return existing is not None
