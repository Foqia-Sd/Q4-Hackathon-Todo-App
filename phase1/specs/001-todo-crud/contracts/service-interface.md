# Service Interface Contract: TodoService

**Branch**: `001-todo-crud` | **Date**: 2025-12-27
**Purpose**: Define the internal API contract between CLI layer and business logic

## Overview

Since this is a console application (no REST API), contracts define the internal service interface. This ensures clear boundaries between layers and enables testing.

## TodoService Interface

### Method: add_todo

**Purpose**: Create a new todo item

```python
def add_todo(self, title: str) -> Todo:
    """
    Create a new todo with the given title.

    Args:
        title: The todo title (must be non-empty after trimming)

    Returns:
        The created Todo object with assigned ID

    Raises:
        ValidationError: If title is empty or whitespace-only
    """
```

| Input | Type | Validation |
|-------|------|------------|
| title | str | Non-empty after strip() |

| Output | Type | Description |
|--------|------|-------------|
| Todo | Todo | Created todo with id, title, completed=False |

| Error Condition | Exception | Message |
|-----------------|-----------|---------|
| Empty title | ValidationError | "Title cannot be empty" |

---

### Method: get_all_todos

**Purpose**: Retrieve all todos in the system

```python
def get_all_todos(self) -> list[Todo]:
    """
    Get all todos.

    Returns:
        List of all Todo objects (may be empty)
    """
```

| Input | Type | Validation |
|-------|------|------------|
| (none) | - | - |

| Output | Type | Description |
|--------|------|-------------|
| List[Todo] | list[Todo] | All todos, empty list if none |

---

### Method: get_todo_by_id

**Purpose**: Retrieve a specific todo by ID

```python
def get_todo_by_id(self, todo_id: int) -> Todo | None:
    """
    Get a todo by its ID.

    Args:
        todo_id: The ID of the todo to retrieve

    Returns:
        The Todo object if found, None otherwise
    """
```

| Input | Type | Validation |
|-------|------|------------|
| todo_id | int | Must be positive integer |

| Output | Type | Description |
|--------|------|-------------|
| Todo \| None | Todo or None | Todo if found, None if not |

---

### Method: update_todo

**Purpose**: Update an existing todo's title

```python
def update_todo(self, todo_id: int, new_title: str) -> Todo:
    """
    Update a todo's title.

    Args:
        todo_id: The ID of the todo to update
        new_title: The new title (must be non-empty after trimming)

    Returns:
        The updated Todo object

    Raises:
        ValidationError: If new_title is empty or whitespace-only
        TodoNotFoundError: If todo with given ID does not exist
    """
```

| Input | Type | Validation |
|-------|------|------------|
| todo_id | int | Must exist in storage |
| new_title | str | Non-empty after strip() |

| Output | Type | Description |
|--------|------|-------------|
| Todo | Todo | Updated todo object |

| Error Condition | Exception | Message |
|-----------------|-----------|---------|
| Empty title | ValidationError | "Title cannot be empty" |
| ID not found | TodoNotFoundError | "Todo not found" |

---

### Method: delete_todo

**Purpose**: Permanently remove a todo

```python
def delete_todo(self, todo_id: int) -> bool:
    """
    Delete a todo by its ID.

    Args:
        todo_id: The ID of the todo to delete

    Returns:
        True if deleted, False if not found
    """
```

| Input | Type | Validation |
|-------|------|------------|
| todo_id | int | None (graceful handling) |

| Output | Type | Description |
|--------|------|-------------|
| bool | bool | True if deleted, False if not found |

---

### Method: toggle_complete

**Purpose**: Toggle a todo's completion status

```python
def toggle_complete(self, todo_id: int) -> Todo:
    """
    Toggle a todo's completion status.

    Args:
        todo_id: The ID of the todo to toggle

    Returns:
        The updated Todo object

    Raises:
        TodoNotFoundError: If todo with given ID does not exist
    """
```

| Input | Type | Validation |
|-------|------|------------|
| todo_id | int | Must exist in storage |

| Output | Type | Description |
|--------|------|-------------|
| Todo | Todo | Todo with toggled completed status |

| Error Condition | Exception | Message |
|-----------------|-----------|---------|
| ID not found | TodoNotFoundError | "Todo not found" |

---

### Method: has_todos

**Purpose**: Check if any todos exist

```python
def has_todos(self) -> bool:
    """
    Check if there are any todos.

    Returns:
        True if at least one todo exists, False otherwise
    """
```

| Input | Type | Validation |
|-------|------|------------|
| (none) | - | - |

| Output | Type | Description |
|--------|------|-------------|
| bool | bool | True if todos exist |

## Exception Definitions

```python
class ValidationError(Exception):
    """Raised when input validation fails."""
    pass

class TodoNotFoundError(Exception):
    """Raised when a requested todo does not exist."""
    pass
```

## Usage Examples

```python
# Initialize service
service = TodoService()

# Add todos
todo1 = service.add_todo("Buy groceries")
todo2 = service.add_todo("Walk the dog")

# View all
todos = service.get_all_todos()  # [todo1, todo2]

# Toggle complete
updated = service.toggle_complete(todo1.id)
assert updated.completed == True

# Update title
updated = service.update_todo(todo1.id, "Buy organic groceries")
assert updated.title == "Buy organic groceries"

# Delete
success = service.delete_todo(todo2.id)
assert success == True

# Check empty (after deletions)
has_any = service.has_todos()  # True (todo1 still exists)
```

## Contract Validation Checklist

| Contract | Spec Requirement | Verified |
|----------|------------------|----------|
| add_todo validates title | FR-011 | ✓ |
| add_todo assigns unique ID | FR-012 | ✓ |
| add_todo sets incomplete default | FR-013 | ✓ |
| get_all_todos returns all | FR-020 | ✓ |
| update_todo validates title | FR-031 | ✓ |
| update_todo preserves on failure | FR-032 | ✓ |
| delete_todo returns success/fail | FR-042, FR-043 | ✓ |
| toggle_complete flips status | FR-051, FR-052 | ✓ |
