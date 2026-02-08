"""Todo service for managing tasks in memory."""

from src.models import Task


class TaskNotFoundError(Exception):
    """Raised when a task ID doesn't exist."""

    def __init__(self, task_id: int) -> None:
        self.task_id = task_id
        super().__init__(f"Task with ID {task_id} not found")


class TodoService:
    """Manages the in-memory collection of tasks."""

    def __init__(self) -> None:
        """Initialize empty task store and ID counter."""
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    def add_task(self, title: str, description: str = "") -> Task:
        """Create new task with auto-assigned ID.

        Args:
            title: The task title (required)
            description: The task description (optional)

        Returns:
            The created Task instance
        """
        task = Task(
            id=self._next_id,
            title=title,
            description=description,
            completed=False,
        )
        self._tasks[self._next_id] = task
        self._next_id += 1
        return task

    def list_tasks(self) -> list[Task]:
        """Return all tasks sorted by ID."""
        return sorted(self._tasks.values(), key=lambda t: t.id)

    def get_task(self, task_id: int) -> Task:
        """Get task by ID.

        Args:
            task_id: The task ID to retrieve

        Returns:
            The Task instance

        Raises:
            TaskNotFoundError: If task doesn't exist
        """
        if task_id not in self._tasks:
            raise TaskNotFoundError(task_id)
        return self._tasks[task_id]

    def update_task(
        self, task_id: int, title: str, description: str | None = None
    ) -> Task:
        """Update task title and optionally description.

        Args:
            task_id: The task ID to update
            title: New title for the task
            description: New description (None = don't change)

        Returns:
            The updated Task instance

        Raises:
            TaskNotFoundError: If task doesn't exist
        """
        task = self.get_task(task_id)
        # Create new Task with updated values (dataclass is immutable-ish)
        new_description = description if description is not None else task.description
        updated_task = Task(
            id=task.id,
            title=title,
            description=new_description,
            completed=task.completed,
        )
        self._tasks[task_id] = updated_task
        return updated_task

    def delete_task(self, task_id: int) -> None:
        """Delete task by ID.

        Args:
            task_id: The task ID to delete

        Raises:
            TaskNotFoundError: If task doesn't exist
        """
        if task_id not in self._tasks:
            raise TaskNotFoundError(task_id)
        del self._tasks[task_id]

    def toggle_complete(self, task_id: int) -> Task:
        """Toggle task completed status.

        Args:
            task_id: The task ID to toggle

        Returns:
            The updated Task instance

        Raises:
            TaskNotFoundError: If task doesn't exist
        """
        task = self.get_task(task_id)
        updated_task = Task(
            id=task.id,
            title=task.title,
            description=task.description,
            completed=not task.completed,
        )
        self._tasks[task_id] = updated_task
        return updated_task
