Project: In-Memory Todo Console App

Core Features (All 5 required):

1. Add task: User provides title and description → auto-assign unique ID
2. List/View tasks: Show all tasks with ID, title, description, status (Pending/Completed)
3. Update task: By ID, modify title and/or description
4. Delete task: By ID
5. Mark as complete/incomplete: By ID, toggle status

Additional Requirements:
- Interactive REPL console loop
- Commands: add, list, update <id>, delete <id>, complete <id>, help, exit
- Proper error handling (invalid ID, missing args, etc.)
- Help command showing usage
- Graceful exit

Project Structure:
- src/__init__.py
- src/main.py → entry point with REPL
- src/todo_manager.py → class handling all operations
- Task model as dataclass or dict with fields: id, title, description, completed (bool)

Acceptance Criteria:
- App runs with `python -m src.main` or similar
- All 5 core features work correctly
- Data persists only during runtime
- Clean, readable, PEP8-compliant code