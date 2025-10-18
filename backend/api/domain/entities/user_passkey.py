from typing import Literal, Optional, List
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
from sqlmodel import Field, JSON, Column, Index
from api.domain.entities.api_base_model import ApiBaseModel
from api.common.utils import get_utc_now
from webauthn.helpers.structs import AuthenticatorTransport


class Credential(BaseModel):
    credential_id: str
    public_key: str
    sigin_count: int
    transports: List[AuthenticatorTransport] = []
    created_at: datetime
    last_used_at: Optional[datetime] = None


class UserPasskey(ApiBaseModel, table=True):
    __tablename__ = "user_passkeys"

    user_email: EmailStr = Field(unique=True, index=True)
    credentials: List[Credential] = Field(default=[], sa_column=Column(JSON))


class Challenges(ApiBaseModel, table=True):
    __tablename__ = "user_passkey_challenges"

    email: EmailStr = Field(index=True)
    type: str = Field(default="registration")
    challenge: str
    expires_at: datetime = Field(
        default_factory=lambda: get_utc_now() + timedelta(minutes=5)
    )

    __table_args__ = (Index("idx_challenges_expires_at", "expires_at"),)
