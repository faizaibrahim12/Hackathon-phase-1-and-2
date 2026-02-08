"""Task business logic service"""
from sqlmodel import Session, select
from datetime import datetime
from typing import Optional
from .models import Task
from ..exceptions import TaskNotFoundError, UnauthorizedAccessException


class TaskService:
    """Service for task operations"""

    @staticmethod
    def create_task(
        session: Session,
        user_id: str,
        title: str,
        description: Optional[str] = None,
        due_date: Optional[str] = None,
    ) -> Task:
        """
        Create a new task for user

        Args:
            session: Database session
            user_id: ID of task owner (as string to match JWT and MCP spec)
            title: Task title
            description: Optional task description
            due_date: Optional due date (ISO format)

        Returns:
            Created Task object
        """
        task = Task(
            user_id=user_id,
            title=title,
            description=description,
            due_date=due_date,
            completed=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def get_task(session: Session, task_id: int, user_id: str) -> Task:
        """
        Get a task by ID (verify ownership)

        Args:
            session: Database session
            task_id: Task ID
            user_id: Current user ID (as string to match JWT and MCP spec)

        Returns:
            Task object

        Raises:
            TaskNotFoundError: If task not found
            UnauthorizedAccessException: If user doesn't own task
        """
        task = session.exec(
            select(Task).where(Task.id == task_id)
        ).first()

        if not task:
            raise TaskNotFoundError()

        if task.user_id != user_id:
            raise UnauthorizedAccessException()

        return task

    @staticmethod
    def list_tasks(
        session: Session,
        user_id: str,
        status: str = "all",
        sort: str = "created",
        order: str = "desc",
    ) -> tuple[list[Task], int]:
        """
        List user's tasks with filtering and sorting

        Args:
            session: Database session
            user_id: User ID to filter by (as string to match JWT and MCP spec)
            status: Filter by status (all/pending/completed)
            sort: Sort by field (created/title)
            order: Sort order (asc/desc)

        Returns:
            Tuple of (tasks list, total count)
        """
        # Build query
        query = select(Task).where(Task.user_id == user_id)

        # Apply status filter
        if status == "pending":
            query = query.where(Task.completed == False)
        elif status == "completed":
            query = query.where(Task.completed == True)

        # Apply sorting
        if sort == "title":
            sort_column = Task.title
        else:  # default to created
            sort_column = Task.created_at

        if order == "asc":
            query = query.order_by(sort_column.asc())
        else:  # default to desc
            query = query.order_by(sort_column.desc())

        # Execute query
        tasks = session.exec(query).all()
        total = len(tasks)

        return tasks, total

    @staticmethod
    def update_task(
        session: Session,
        task_id: int,
        user_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        due_date: Optional[str] = None,
        completed: Optional[bool] = None,
    ) -> Task:
        """
        Update a task

        Args:
            session: Database session
            task_id: Task ID
            user_id: Current user ID (as string to match JWT and MCP spec)
            title: New title (optional)
            description: New description (optional)
            due_date: New due date (optional)
            completed: New completion status (optional)

        Returns:
            Updated Task object

        Raises:
            TaskNotFoundError: If task not found
            UnauthorizedAccessException: If user doesn't own task
        """
        task = TaskService.get_task(session, task_id, user_id)

        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if due_date is not None:
            task.due_date = due_date
        if completed is not None:
            task.completed = completed

        task.updated_at = datetime.utcnow()

        session.add(task)
        session.commit()
        session.refresh(task)

        return task

    @staticmethod
    def toggle_task(session: Session, task_id: int, user_id: str) -> Task:
        """
        Toggle task completion status

        Args:
            session: Database session
            task_id: Task ID
            user_id: Current user ID (as string to match JWT and MCP spec)

        Returns:
            Updated Task object

        Raises:
            TaskNotFoundError: If task not found
            UnauthorizedAccessException: If user doesn't own task
        """
        task = TaskService.get_task(session, task_id, user_id)
        task.completed = not task.completed
        task.updated_at = datetime.utcnow()

        session.add(task)
        session.commit()
        session.refresh(task)

        return task

    @staticmethod
    def delete_task(session: Session, task_id: int, user_id: str) -> None:
        """
        Delete a task

        Args:
            session: Database session
            task_id: Task ID
            user_id: Current user ID (as string to match JWT and MCP spec)

        Raises:
            TaskNotFoundError: If task not found
            UnauthorizedAccessException: If user doesn't own task
        """
        task = TaskService.get_task(session, task_id, user_id)
        session.delete(task)
        session.commit()
