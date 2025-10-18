from typing import Optional
from uuid import UUID

from api.common.base_repository import BaseRepository
from api.common.utils import get_logger
from api.domain.entities.storage_settings import StorageProvider, StorageSettings

logger = get_logger(__name__)


class StorageSettingsRepository(BaseRepository[StorageSettings]):
    def __init__(self):
        super().__init__(StorageSettings)

    async def configure_storage(self, setting: StorageSettings) -> UUID:
        """配置存储设置"""
        existing: Optional[StorageSettings] = await self.single_or_none(
            provider=setting.provider.value
        )
        logger.info(f"Existing setting found: {existing}")
        if existing is None:
            setting_data = setting.model_dump()
            result = await super().create(setting_data)
            return result.id

        logger.info(f"Updating existing setting for provider: {setting.provider.value}")
        result = await self.update(existing.id, setting.model_dump())
        logger.info(f"Update result: {result.id} document(s) modified.")
        return result.id

    async def get_storages(self) -> list[StorageSettings]:
        """获取所有存储设置"""
        settings = await self.get_all()
        logger.info(f"Retrieved {len(settings)} storage settings.")
        return settings

    async def get_storage_by_provider(
        self, provider: StorageProvider
    ) -> Optional[StorageSettings]:
        """根据提供商获取存储设置"""
        setting: Optional[StorageSettings] = await self.single_or_none(
            provider=provider.value
        )
        if setting is None:
            logger.warning(f"No storage setting found for provider: {provider.value}")
        return setting
