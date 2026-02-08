from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum


class RoleEnum(str, Enum):
    user = "user"
    assistant = "assistant"


class Conversation(SQLModel, table=True):
    """Conversation model for chat sessions"""
    __tablename__ = "conversations"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)  # Using string for user_id as per MCP spec
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Message(SQLModel, table=True):
    """Message model for chat history"""
    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)  # Using string for user_id as per MCP spec
    conversation_id: int = Field(foreign_key="conversations.id", index=True)
    role: RoleEnum = Field(sa_column_kwargs={"name": "role"})  # user or assistant
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)


class Task(SQLModel, table=True):
    """Task model for todo items (enhanced for chatbot)"""
    __tablename__ = "tasks_chatbot"  # Using different table name to avoid conflicts

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)  # Using string for user_id as per MCP spec
    title: str = Field(max_length=255)
    description: Optional[str] = Field(default=None, max_length=5000)
    completed: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow)