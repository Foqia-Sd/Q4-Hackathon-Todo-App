# Data Model: Phase 1 In-Memory Todo CRUD Application

**Branch**: `001-todo-crud` | **Date**: 2025-12-27
**Source**: [spec.md](./spec.md) Key Entities section

## Entity Overview

Phase 1 defines a minimal data model with one primary entity (Todo) and one collection container (TodoList/MemoryStore).

## Entities

### Todo

The primary entity representing a task to be completed.

| Attribute | Type | Constraints | Description |
|-----------|------|-------------|-------------|
| id | int | Unique, immutable, auto-generated, never reused | System-assigned identifier |
| title | str | Non-empty, user-provided | Task description |
| completed | bool | Default: False | Completion status |

**Invariants**:
- `id` MUST be assigned by the system, never by the user
- `id` MUST remain constant for the lifetime of the todo
- `id` MUST never be reused within a session (even after deletion)
- `title` MUST be a non-empty string after whitespace trimming
- `completed` MUST be exactly `True` or `False`

**State Transitions**:

```
                    ┌─────────────────┐
     create()       │                 │
    ──────────────► │   INCOMPLETE    │
                    │ (completed=False)│
                    └────────┬────────┘
                             │
                    toggle() │ toggle()
                             ▼
                    ┌─────────────────┐
                    │                 │
                    │    COMPLETE     │
                    │ (completed=True) │
                    └─────────────────┘
```

**Python Implementation Guidance**:

```python
from dataclasses import dataclass, field

@dataclass
class Todo:
    """Represents a single todo item."""
    id: int
    title: str
    completed: bool = False

    def toggle(self) -> None:
        """Toggle completion status."""
        self.completed = not self.completed
```

### MemoryStore (TodoList)

The in-memory collection container for all todos.

| Attribute | Type | Constraints | Description |
|-----------|------|-------------|-------------|
| _todos | Dict[int, Todo] | Private | Maps todo ID to Todo object |
| _next_id | int | Private, starts at 1 | Next available ID |

**Operations**:

| Operation | Input | Output | Description |
|-----------|-------|--------|-------------|
| add | Todo (without id) | int (assigned id) | Add new todo, assign ID |
| get_all | - | List[Todo] | Return all todos |
| get_by_id | int | Todo \| None | Find todo by ID |
| update | int, Todo | bool | Update existing todo |
| delete | int | bool | Remove todo by ID |
| count | - | int | Return number of todos |
| is_empty | - | bool | Check if no todos exist |

**Python Implementation Guidance**:

```python
class MemoryStore:
    """In-memory storage for todos."""

    def __init__(self) -> None:
        self._todos: dict[int, Todo] = {}
        self._next_id: int = 1

    def add(self, title: str) -> Todo:
        """Add a new todo and return it with assigned ID."""
        todo = Todo(id=self._next_id, title=title)
        self._todos[self._next_id] = todo
        self._next_id += 1
        return todo

    def get_all(self) -> list[Todo]:
        """Return all todos in insertion order."""
        return list(self._todos.values())

    def get_by_id(self, todo_id: int) -> Todo | None:
        """Return todo by ID or None if not found."""
        return self._todos.get(todo_id)

    def update(self, todo_id: int, title: str) -> Todo | None:
        """Update todo title, return updated todo or None."""
        todo = self._todos.get(todo_id)
        if todo:
            todo.title = title
        return todo

    def delete(self, todo_id: int) -> bool:
        """Delete todo by ID, return True if deleted."""
        if todo_id in self._todos:
            del self._todos[todo_id]
            return True
        return False

    def count(self) -> int:
        """Return number of todos."""
        return len(self._todos)

    def is_empty(self) -> bool:
        """Return True if no todos exist."""
        return len(self._todos) == 0
```

## Validation Rules

### Title Validation

| Rule | Check | Error Message |
|------|-------|---------------|
| Non-empty | `title.strip() != ""` | "Title cannot be empty" |
| Non-whitespace-only | `title.strip() != ""` | "Title cannot be empty" |

**Validation Function**:

```python
class ValidationError(Exception):
    """Raised when validation fails."""
    pass

def validate_title(title: str) -> str:
    """
    Validate and normalize a todo title.

    Returns cleaned title if valid.
    Raises ValidationError if invalid.
    """
    cleaned = title.strip()
    if not cleaned:
        raise ValidationError("Title cannot be empty")
    return cleaned
```

## Relationships

```
┌──────────────────────────────────────────────────────────┐
│                      MemoryStore                          │
│                                                          │
│  _todos: Dict[int, Todo]                                 │
│                                                          │
│     1 ──────────────────────────── 0..* Todo             │
│    (store)                        (contained todos)      │
│                                                          │
│  Relationship: Composition                               │
│  - Store owns all todos                                  │
│  - Todos cannot exist outside store                      │
│  - Store deletion destroys all todos                     │
└──────────────────────────────────────────────────────────┘
```

## Data Lifecycle

| Event | Effect on Data |
|-------|----------------|
| Application start | Empty store created, `_next_id = 1` |
| Add todo | New Todo created with unique ID, stored in dict |
| View todos | Read-only access to all todos |
| Update todo | Title field modified on existing todo |
| Toggle complete | Completed field flipped on existing todo |
| Delete todo | Todo removed from dict, ID never reused |
| Application exit | All data destroyed (in-memory only) |

## Alignment with Requirements

| Requirement | Data Model Support |
|-------------|-------------------|
| FR-001 (unique ID) | `_next_id` counter, never reused |
| FR-002 (title required) | `validate_title()` enforces non-empty |
| FR-003 (completion status) | `completed: bool` with default False |
| FR-004 (stable ID) | ID assigned once, never modified |
| FR-005 (ID never reused) | `_next_id` only increments |
| FR-070 (in-memory only) | `Dict[int, Todo]` in Python memory |
| FR-071 (no persistence) | No save/load methods |
| FR-072 (no file I/O) | No file operations in data layer |
