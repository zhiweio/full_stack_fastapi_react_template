from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field
from sqlalchemy import DateTime, func
from uuid import UUID, uuid4


class ApiBaseModel(SQLModel):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(
        default_factory=datetime.utcnow, sa_column_kwargs={"server_default": func.now()}
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": func.now()}
    )
    tenant_id: Optional[UUID] = Field(default=None, foreign_key="tenants.id")

    class Config:
        from_attributes = True

    def to_serializable_dict(self):
        """Convert model to serializable dictionary"""
        data = self.model_dump()
        data["id"] = str(self.id) if self.id else None
        data["created_at"] = self.created_at.isoformat() if self.created_at else None
        data["updated_at"] = self.updated_at.isoformat() if self.updated_at else None
        if self.tenant_id:
            data["tenant_id"] = str(self.tenant_id)
        return data
