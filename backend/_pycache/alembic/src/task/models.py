from sqlmodel import SQLModel, Field
from datetime import datetime, date
from typing import Optional


class TaskBase(SQLModel):
    """Base model for Task"""
    title: str = Field(max_length=255)
    description: Optional[str] = Field(default=None, max_length=5000)
    completed: bool = Field(default=False)


class Task(TaskBase, table=True):
    """Task model for todo items"""
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)  # Changed to string to match MCP spec
    due_date: Optional[date] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": "ziakhan",
                "title": "Learn FastAPI",
                "description": "Study async framework",
                "completed": False,
                "due_date": "2025-01-15",
                "created_at": "2025-01-07T10:00:00",
                "updated_at": "2025-01-07T10:00:00",
            }
        }


class TaskCreate(TaskBase):
    """Model for creating a new task"""
    title: str


class TaskUpdate(SQLModel):
    """Model for updating an existing task"""
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
