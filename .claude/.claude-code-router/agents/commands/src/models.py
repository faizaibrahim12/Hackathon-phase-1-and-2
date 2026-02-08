"""Data models for the Todo application."""

from dataclasses import dataclass


@dataclass
class Task:
    """Represents a todo item."""

    id: int
    title: str
    description: str = ""
    completed: bool = False

    def status_display(self) -> str:
        """Return 'Completed' or 'Pending' based on completed flag."""
        return "Completed" if self.completed else "Pending"
