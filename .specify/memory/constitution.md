# In-Memory Todo Console App Constitution

## Core Principles

### I. Pure Python
All implementation uses Python 3.13+ standard library only. No external dependencies. Code must be self-contained and portable.

### II. In-Memory Only
All data storage is ephemeral - tasks exist only during runtime. No file I/O, no databases, no persistence. This is by design for simplicity.

### III. REPL-First Interface
The application operates as an interactive command loop. Text in via stdin, text out via stdout, errors to stderr. Clean, predictable I/O patterns.

### IV. Test-First Development
TDD is mandatory: Write tests first, verify they fail, then implement. Red-Green-Refactor cycle strictly enforced. All features must have corresponding tests.

### V. Modular Architecture
Separation of concerns enforced:
- `main.py`: Entry point, REPL loop, command parsing
- `todo_manager.py`: Business logic, task CRUD operations
- `task.py`: Data model (dataclass)

No god objects. Each module has single responsibility.

### VI. User-Friendly Errors
No stack traces in normal operation. All errors display human-readable messages with actionable guidance. Invalid input should suggest correct usage.

## Code Standards

### Style
- PEP 8 compliance mandatory
- Type hints for all function signatures
- Docstrings for public methods
- Clear, descriptive variable names

### Testing
- Unit tests for all TodoManager methods
- Integration tests for REPL commands
- Edge case coverage required
- Tests live in `tests/` directory

### Error Handling
- Validate all user input
- Catch and handle expected exceptions
- Provide usage hints on invalid commands
- Graceful handling of Ctrl+C (KeyboardInterrupt)

## Constraints

- Python 3.13+ required
- No third-party packages
- No persistence layer
- No network operations
- Single-user, single-threaded

## Governance

Constitution guides all development decisions. Simplicity over complexity. YAGNI principle applies - implement only what's specified.

**Version**: 1.0.0 | **Ratified**: 2025-12-27 | **Last Amended**: 2025-12-27
