from sqlmodel import SQLModel, Field
from datetime import datetime, timedelta
from typing import Optional
import uuid


class RefreshToken(SQLModel, table=True):
    """Refresh token model for authentication"""
    __tablename__ = "refresh_tokens"

    id: Optional[int] = Field(default=None, primary_key=True)
    token: str = Field(unique=True, index=True, max_length=255)
    user_id: int = Field(index=True)
    expires_at: datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)
    revoked: bool = Field(default=False)

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "token": "unique-refresh-token-string",
                "user_id": 1,
                "expires_at": "2025-01-14T10:00:00",
                "created_at": "2025-01-07T10:00:00",
                "revoked": False
            }
        }


def generate_refresh_token() -> str:
    """Generate a unique refresh token"""
    return str(uuid.uuid4())


def get_default_refresh_token_expiry() -> datetime:
    """Get default refresh token expiry (30 days)"""
    return datetime.utcnow() + timedelta(days=30)