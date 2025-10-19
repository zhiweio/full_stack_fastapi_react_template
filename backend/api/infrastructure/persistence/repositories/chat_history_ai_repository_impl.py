from api.common.base_repository import BaseRepository
from api.domain.entities.ai import ChatHistoryAI
from sqlalchemy.ext.asyncio import AsyncSession


class ChatHistoryAIRepository(BaseRepository[ChatHistoryAI]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(ChatHistoryAI, session)
