from typing import Any, Optional
from api.common.utils import validate_uuid

from api.common.base_repository import BaseRepository
from api.common.utils import get_logger
from api.domain.entities.user_preference import UserPreference

logger = get_logger(__name__)


class UserPreferenceRepository(BaseRepository[UserPreference]):
    def __init__(self):
        super().__init__(UserPreference)

    async def get_preferences(self, user_id: str) -> Optional[UserPreference]:
        """获取用户偏好设置"""
        validated_user_id = validate_uuid(user_id, "User ID")
        user_pref = await self.single_or_none(user_id=validated_user_id)
        return user_pref

    async def set_preferences(self, user_id: str, preferences: dict[str, Any]) -> None:
        """设置用户偏好"""
        validated_user_id = validate_uuid(user_id, "User ID")
        existing = await self.single_or_none(user_id=validated_user_id)
        if existing is None:
            pref_data = {"user_id": validated_user_id, "preferences": preferences}
            await super().create(pref_data)
            return
        await self.update(existing.id, {"preferences": preferences})
