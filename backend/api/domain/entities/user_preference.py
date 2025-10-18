from typing import Any, Dict
from uuid import UUID
from sqlmodel import Field, JSON, Column
from api.domain.entities.api_base_model import ApiBaseModel


class UserPreference(ApiBaseModel, table=True):
    __tablename__ = "user_preferences"

    user_id: UUID = Field(foreign_key="users.id", unique=True, index=True)
    preferences: Dict[str, Any] = Field(default={}, sa_column=Column(JSON))

    def to_serializable_dict(self):
        base_doc = super().to_serializable_dict()
        return {
            **base_doc,
            "user_id": str(self.user_id),
            "preferences": self.preferences or {},
        }
