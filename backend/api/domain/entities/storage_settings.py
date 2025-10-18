from enum import Enum
from typing import Optional
from sqlmodel import Field
from api.domain.dtos.storage_settings_dto import AvailableStorageProviderDTO
from api.domain.entities.api_base_model import ApiBaseModel


class StorageProvider(str, Enum):
    AWS_S3 = "s3"
    AZURE_BLOB = "azure_blob"


class StorageSettings(ApiBaseModel, table=True):
    __tablename__ = "storage_settings"

    provider: StorageProvider
    is_enabled: bool = Field(default=False)
    region: str
    aws_access_key: Optional[str] = None
    aws_secret_key: Optional[str] = None
    aws_bucket_name: Optional[str] = None
    azure_connection_string: Optional[str] = None
    azure_container_name: Optional[str] = None

    def to_serializable_dict(self) -> AvailableStorageProviderDTO:
        base_doc = super().to_serializable_dict()
        result = {
            **base_doc,
            "provider": self.provider.value,
            "is_enabled": self.is_enabled,
            "region": self.region,
            "aws_access_key": self.aws_access_key,
            "aws_secret_key": self.aws_secret_key,
            "aws_bucket_name": self.aws_bucket_name,
            "azure_connection_string": self.azure_connection_string,
            "azure_container_name": self.azure_container_name,
        }
        return AvailableStorageProviderDTO(**result)
