"""Task API routes"""
from fastapi import APIRouter, Depends, Request, Header, status
from sqlmodel import Session
from typing import Optional
from .schemas import (
    TaskCreate,
    TaskUpdate,
    TaskResponse,
    TaskListResponse,
)
from .service import TaskService
from ..database import get_session

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


def get_user_id(request: Request) -> str:
    """Extract user_id from request state (set by auth middleware) and convert to string"""
    return str(request.state.user_id)


@router.get("")
async def list_tasks(
    request: Request,
    status_filter: str = "all",
    sort: str = "created",
    order: str = "desc",
    session: Session = Depends(get_session),
) -> TaskListResponse:
    """
    List user's tasks with filtering and sorting

    Args:
        request: HTTP request (contains user_id in state)
        status_filter: Filter by status (all/pending/completed)
        sort: Sort by field (created/title)
        order: Sort order (asc/desc)
        session: Database session

    Returns:
        TaskListResponse with tasks array and total count
    """
    user_id = get_user_id(request)
    tasks, total = TaskService.list_tasks(
        session,
        user_id,
        status=status_filter,
        sort=sort,
        order=order,
    )

    return TaskListResponse(
        tasks=[
            TaskResponse(
                id=task.id,
                user_id=task.user_id,
                title=task.title,
                description=task.description,
                completed=task.completed,
                due_date=task.due_date,
                created_at=task.created_at,
                updated_at=task.updated_at,
            )
            for task in tasks
        ],
        total=total,
    )


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_task(
    request: Request,
    task_input: TaskCreate,
    session: Session = Depends(get_session),
) -> TaskResponse:
    """
    Create a new task

    Args:
        request: HTTP request (contains user_id in state)
        task_input: Task creation request
        session: Database session

    Returns:
        Created TaskResponse
    """
    user_id = get_user_id(request)
    task = TaskService.create_task(
        session,
        user_id,
        task_input.title,
        task_input.description,
        task_input.due_date,
    )

    return TaskResponse(
        id=task.id,
        user_id=task.user_id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        due_date=task.due_date,
        created_at=task.created_at,
        updated_at=task.updated_at,
    )


@router.patch("/{task_id}")
async def update_task(
    request: Request,
    task_id: int,
    task_input: TaskUpdate,
    session: Session = Depends(get_session),
) -> TaskResponse:
    """
    Update a task

    Args:
        request: HTTP request (contains user_id in state)
        task_id: Task ID to update
        task_input: Task update request
        session: Database session

    Returns:
        Updated TaskResponse
    """
    user_id = get_user_id(request)
    task = TaskService.update_task(
        session,
        task_id,
        user_id,
        task_input.title,
        task_input.description,
        task_input.due_date,
        task_input.completed,
    )

    return TaskResponse(
        id=task.id,
        user_id=task.user_id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        due_date=task.due_date,
        created_at=task.created_at,
        updated_at=task.updated_at,
    )


@router.patch("/{task_id}/toggle")
async def toggle_task(
    request: Request,
    task_id: int,
    session: Session = Depends(get_session),
) -> TaskResponse:
    """
    Toggle task completion status

    Args:
        request: HTTP request (contains user_id in state)
        task_id: Task ID to toggle
        session: Database session

    Returns:
        Updated TaskResponse
    """
    user_id = get_user_id(request)
    task = TaskService.toggle_task(session, task_id, user_id)

    return TaskResponse(
        id=task.id,
        user_id=task.user_id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        due_date=task.due_date,
        created_at=task.created_at,
        updated_at=task.updated_at,
    )


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    request: Request,
    task_id: int,
    session: Session = Depends(get_session),
):
    """
    Delete a task

    Args:
        request: HTTP request (contains user_id in state)
        task_id: Task ID to delete
        session: Database session

    Returns:
        None (204 No Content)
    """
    user_id = get_user_id(request)
    TaskService.delete_task(session, task_id, user_id)
