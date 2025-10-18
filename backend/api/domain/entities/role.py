from typing import List, Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship
from sqlalchemy import JSON, Column
from api.domain.entities.api_base_model import ApiBaseModel
from api.domain.enum.permission import Permission

if TYPE_CHECKING:
    from .user import User


class Role(ApiBaseModel, table=True):
    __tablename__ = "roles"

    name: str = Field(unique=True, index=True, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    permissions: List[Permission] = Field(
        default=[Permission.USER_VIEW_ONLY, Permission.ROLE_VIEW_ONLY],
        sa_column=Column(JSON),
    )

    # 关系定义
    users: List["User"] = Relationship(back_populates="role")

    def to_serializable_dict(self):
        base_doc = super().to_serializable_dict()
        return {
            **base_doc,
            "name": self.name,
            "description": self.description,
            "permissions": [
                perm.value if hasattr(perm, "value") else perm
                for perm in self.permissions
            ],
        }
