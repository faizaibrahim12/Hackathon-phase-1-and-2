"""Utility functions for parsing and formatting."""

import shlex
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models import Task


def parse_command(input_str: str) -> tuple[str, str]:
    """Split input into (command, remaining_args).

    Returns ('', '') for empty input.
    Example: 'add "Buy milk" "From store"' -> ('add', '"Buy milk" "From store"')
    """
    stripped = input_str.strip()
    if not stripped:
        return ("", "")

    parts = stripped.split(maxsplit=1)
    command = parts[0].lower()
    args = parts[1] if len(parts) > 1 else ""
    return (command, args)


def parse_quoted_args(args_str: str) -> list[str]:
    """Parse arguments respecting quoted strings.

    Example: '"Buy milk" "From store"' -> ['Buy milk', 'From store']
    Example: 'Buy milk' -> ['Buy', 'milk'] (unquoted splits on space)
    Uses shlex for robust parsing.
    """
    if not args_str.strip():
        return []

    try:
        return shlex.split(args_str)
    except ValueError:
        # Handle unmatched quotes by splitting on whitespace
        return args_str.split()


def validate_id(id_str: str) -> int | None:
    """Convert string to positive int, or None if invalid.

    Example: '5' -> 5
    Example: 'abc' -> None
    Example: '-1' -> None
    Example: '0' -> None
    """
    try:
        value = int(id_str.strip())
        return value if value > 0 else None
    except (ValueError, AttributeError):
        return None


def format_task_table(tasks: list["Task"]) -> str:
    """Format tasks as aligned table for display.

    Returns formatted string with headers and rows.
    """
    if not tasks:
        return "No tasks yet."

    # Calculate column widths
    id_width = max(len("ID"), max(len(str(t.id)) for t in tasks))
    title_width = max(len("Title"), max(len(t.title) for t in tasks))
    desc_width = max(len("Description"), max(len(t.description) for t in tasks))
    status_width = len("Completed")  # Longest status string

    # Build header
    header = (
        f"{'ID':<{id_width}}  "
        f"{'Title':<{title_width}}  "
        f"{'Description':<{desc_width}}  "
        f"{'Status':<{status_width}}"
    )
    separator = "-" * len(header)

    # Build rows
    rows = []
    for task in tasks:
        row = (
            f"{task.id:<{id_width}}  "
            f"{task.title:<{title_width}}  "
            f"{task.description:<{desc_width}}  "
            f"{task.status_display():<{status_width}}"
        )
        rows.append(row)

    return "\n".join([header, separator] + rows)
