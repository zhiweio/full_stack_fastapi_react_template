from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship
from sqlalchemy import Index
from pydantic import EmailStr
from uuid import UUID
from api.common.enums.gender import Gender
from api.domain.entities.api_base_model import ApiBaseModel

if TYPE_CHECKING:
    from .role import Role
    from .tenant import Tenant


class User(ApiBaseModel, table=True):
    __tablename__ = "users"

    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    gender: Gender = Field(index=True)
    role_id: Optional[UUID] = Field(default=None, foreign_key="roles.id")
    is_active: bool = Field(default=True)
    activated_at: Optional[datetime] = None
    image_url: Optional[str] = Field(default=None, max_length=500)
    password: str = Field(max_length=255)  # hashed password

    # 关系定义
    role: Optional["Role"] = Relationship(back_populates="users")
    tenant: Optional["Tenant"] = Relationship(back_populates="users")

    # 索引定义
    __table_args__ = (
        Index("idx_user_email_tenant", "email", "tenant_id", unique=True),
        Index("idx_user_gender", "gender"),
        Index("idx_user_active", "is_active"),
    )

    def to_serializable_dict(self):
        base_doc = super().to_serializable_dict()
        return {
            **base_doc,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "gender": str(self.gender.value),
            "role_id": str(self.role_id) if self.role_id else None,
            "is_active": self.is_active,
            "activated_at": self.activated_at.isoformat()
            if self.activated_at
            else None,
            "image_url": self.image_url,
        }
