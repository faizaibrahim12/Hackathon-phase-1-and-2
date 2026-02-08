

"""Main entry point for the Todo Console App."""

from src.todo_service import TodoService, TaskNotFoundError
from src.utils import parse_command, parse_quoted_args, validate_id, format_task_table


def _handle_add(service: TodoService, args: str) -> str:
    """Handle 'add' command. Returns success/error message."""
    parsed = parse_quoted_args(args)

    if not parsed:
        return "Usage: add <title> [description]"

    title = parsed[0]
    description = parsed[1] if len(parsed) > 1 else ""

    task = service.add_task(title, description)
    return f"Task {task.id} created successfully."


def _handle_list(service: TodoService) -> str:
    """Handle 'list' command. Returns formatted task table."""
    tasks = service.list_tasks()
    return format_task_table(tasks)


def _handle_update(service: TodoService, args: str) -> str:
    """Handle 'update' command. Returns success/error message."""
    parsed = parse_quoted_args(args)

    if len(parsed) < 2:
        return "Usage: update <id> <title> [description]"

    task_id = validate_id(parsed[0])
    if task_id is None:
        return "Error: Invalid ID. Please provide a numeric task ID."

    title = parsed[1]
    description = parsed[2] if len(parsed) > 2 else None

    try:
        service.update_task(task_id, title, description)
        return f"Task {task_id} updated successfully."
    except TaskNotFoundError:
        return f"Error: Task with ID {task_id} not found."


def _handle_delete(service: TodoService, args: str) -> str:
    """Handle 'delete' command. Returns success/error message."""
    parsed = parse_quoted_args(args)

    if not parsed:
        return "Usage: delete <id>"

    task_id = validate_id(parsed[0])
    if task_id is None:
        return "Error: Invalid ID. Please provide a numeric task ID."

    try:
        service.delete_task(task_id)
        return f"Task {task_id} deleted successfully."
    except TaskNotFoundError:
        return f"Error: Task with ID {task_id} not found."


def _handle_complete(service: TodoService, args: str) -> str:
    """Handle 'complete' command. Returns success/error message."""
    parsed = parse_quoted_args(args)

    if not parsed:
        return "Usage: complete <id>"

    task_id = validate_id(parsed[0])
    if task_id is None:
        return "Error: Invalid ID. Please provide a numeric task ID."

    try:
        task = service.toggle_complete(task_id)
        status = task.status_display()
        return f"Task {task_id} marked as {status}."
    except TaskNotFoundError:
        return f"Error: Task with ID {task_id} not found."


def _handle_help() -> str:
    """Return help text with all commands."""
    return """Available Commands:
  add <title> [description]  - Create a new task
  list                       - Show all tasks
  update <id> <title> [desc] - Update a task
  delete <id>                - Delete a task
  complete <id>              - Toggle task completion
  help                       - Show this help message
  exit                       - Exit the application

Examples:
  add "Buy groceries" "Milk, eggs, bread"
  update 1 "Buy more groceries"
  complete 1
  delete 1"""


def main() -> None:
    """Run the REPL loop."""
    print("Welcome to Todo Console App!")
    print("Type 'help' for available commands.\n")

    service = TodoService()

    while True:
        try:
            user_input = input("todo> ")
            command, args = parse_command(user_input)

            if not command:
                # Empty input, continue silently
                continue

            if command == "exit":
                print("Goodbye!")
                break
            elif command == "help":
                print(_handle_help())
            elif command == "add":
                print(_handle_add(service, args))
            elif command == "list":
                print(_handle_list(service))
            elif command == "update":
                print(_handle_update(service, args))
            elif command == "delete":
                print(_handle_delete(service, args))
            elif command == "complete":
                print(_handle_complete(service, args))
            else:
                print(f"Unknown command: '{command}'. Type 'help' for available commands.")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()
