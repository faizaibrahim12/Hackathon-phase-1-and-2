from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum


class RoleEnum(str, Enum):
    user = "user"
    assistant = "assistant"


class ConversationBase(SQLModel):
    """Base model for Conversation"""
    user_id: str = Field(index=True)


class Conversation(ConversationBase, table=True):
    """Conversation model for chat sessions"""
    __tablename__ = "conversations"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ConversationCreate(ConversationBase):
    """Model for creating a new conversation"""
    user_id: str


class MessageBase(SQLModel):
    """Base model for Message"""
    conversation_id: int = Field(foreign_key="conversations.id", index=True)
    role: str  # "user" or "assistant"
    content: str


class Message(MessageBase, table=True):
    """Message model for chat history"""
    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    conversation_id: int = Field(foreign_key="conversations.id", index=True)
    role: str = Field(sa_column_kwargs={"name": "role"})  # "user" or "assistant"
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)


class MessageCreate(MessageBase):
    """Model for creating a new message"""
    user_id: str
    conversation_id: int
    role: str
    content: str