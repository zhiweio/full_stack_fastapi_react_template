from datetime import datetime
from uuid import UUID
from sqlmodel import Field
from api.domain.entities.api_base_model import ApiBaseModel


class UserPasswordReset(ApiBaseModel, table=True):
    __tablename__ = "user_password_resets"

    user_id: UUID = Field(foreign_key="users.id", index=True)
    token_secret: str
    reset_secret_updated_at: datetime
    first_name: str

    def to_serializable_dict(self):
        base_doc = super().to_serializable_dict()
        return {
            **base_doc,
            "user_id": str(self.user_id),
            "token_secret": self.token_secret,
            "reset_secret_updated_at": self.reset_secret_updated_at.isoformat(),
            "first_name": self.first_name,
        }
