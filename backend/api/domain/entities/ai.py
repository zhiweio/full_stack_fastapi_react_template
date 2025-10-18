from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4
from sqlmodel import Field, JSON, Column, SQLModel
from sqlalchemy import DateTime, func
from pydantic import BaseModel


class ChatSessionAI(SQLModel, table=True):
    __tablename__ = "chat_sessions_ai"

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    session_id: UUID = Field(unique=True, index=True)
    user_id: UUID = Field(foreign_key="users.id")
    history_id: UUID = Field(foreign_key="chat_histories_ai.id")
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(
            "created_at", DateTime(timezone=True), server_default=func.now()
        ),
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column("updated_at", DateTime(timezone=True), onupdate=func.now()),
    )
    tenant_id: Optional[UUID] = Field(default=None, foreign_key="tenants.id")

    class Config:
        from_attributes = True

    def to_serializable_dict(self):
        """Convert model to serializable dictionary"""
        data = self.model_dump()
        data["id"] = str(self.id) if self.id else None
        data["session_id"] = str(self.session_id)
        data["user_id"] = str(self.user_id)
        data["history_id"] = str(self.history_id)
        data["created_at"] = self.created_at.isoformat() if self.created_at else None
        data["updated_at"] = self.updated_at.isoformat() if self.updated_at else None
        if self.tenant_id:
            data["tenant_id"] = str(self.tenant_id)
        return data


class History(BaseModel):
    uid: str
    query: str
    response: str
    timestamp: datetime

    def to_serializable_dict(self):
        return {
            "uid": str(self.uid),
            "query": self.query,
            "response": self.response,
            "timestamp": self.timestamp.isoformat(),
        }


class ChatHistoryAI(SQLModel, table=True):
    __tablename__ = "chat_histories_ai"

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    histories: List[History] = Field(default=[], sa_column=Column(JSON))
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(
            "created_at", DateTime(timezone=True), server_default=func.now()
        ),
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column("updated_at", DateTime(timezone=True), onupdate=func.now()),
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
        data["histories"] = [
            history.to_serializable_dict() for history in self.histories
        ]
        return data


class AISessions(BaseModel):
    # Copy fields from ChatSessionAI for serialization
    id: str
    session_id: str
    user_id: str
    history_id: str
    created_at: str
    updated_at: str
    tenant_id: str | None = None
    sessions: List[ChatHistoryAI] = []
