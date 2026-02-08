from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional


class TaskCreate(BaseModel):
    """Create task request"""
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=5000)
    due_date: Optional[date] = None


class TaskUpdate(BaseModel):
    """Update task request"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=5000)
    due_date: Optional[date] = None
    completed: Optional[bool] = None


class TaskResponse(BaseModel):
    """Task response"""
    id: int
    user_id: str
    title: str
    description: Optional[str]
    completed: bool
    due_date: Optional[date]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TaskListResponse(BaseModel):
    """Task list response"""
    tasks: list[TaskResponse]
    total: int
