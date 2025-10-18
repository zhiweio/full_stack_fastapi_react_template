from datetime import datetime, timedelta
from uuid import UUID
from sqlmodel import Field, Index
from api.domain.entities.api_base_model import ApiBaseModel
from api.common.utils import get_utc_now


class UserMagicLink(ApiBaseModel, table=True):
    __tablename__ = "user_magic_links"

    user_id: UUID = Field(foreign_key="users.id", index=True)
    token: str = Field(unique=True, index=True)
    expires_at: datetime = Field(
        default_factory=lambda: get_utc_now() + timedelta(minutes=15)
    )

    __table_args__ = (Index("idx_expires_at", "expires_at"),)
