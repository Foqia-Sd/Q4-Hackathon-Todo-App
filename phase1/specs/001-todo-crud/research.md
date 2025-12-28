# Research: Phase 1 In-Memory Todo CRUD Application

**Branch**: `001-todo-crud` | **Date**: 2025-12-27
**Purpose**: Resolve technical decisions and document best practices for implementation

## Research Summary

This Phase 1 application has minimal research requirements due to intentionally constrained scope. All technical decisions are straightforward with well-established best practices.

## Decisions

### 1. Python Version

**Decision**: Python 3.11+
**Rationale**:
- Latest stable version with performance improvements
- Full support for type hints and dataclasses
- Dict maintains insertion order (guaranteed since 3.7)
- Wide availability on all target platforms

**Alternatives Considered**:
- Python 3.10: Viable but lacks some 3.11 optimizations
- Python 3.12: Too new, potential compatibility issues with dependencies

### 2. Project Structure

**Decision**: Flat src/ layout with logical layer separation
**Rationale**:
- Simple for small project
- Clear separation of concerns without over-engineering
- Easy to navigate and test
- Follows Python packaging best practices

**Alternatives Considered**:
- Monolithic single file: Too disorganized for maintainability
- Package per feature: Over-engineered for Phase 1 scope

### 3. ID Generation Strategy

**Decision**: Auto-incrementing integer starting at 1
**Rationale**:
- Simple and predictable for users
- Easy to implement with instance counter
- Meets FR-001 (unique), FR-004 (stable), FR-005 (never reused)
- Sufficient for in-memory, single-session use

**Alternatives Considered**:
- UUID: Overkill for single-session; harder for users to reference
- Timestamp-based: Potential collisions; harder to read

### 4. Storage Implementation

**Decision**: Dict[int, Todo] with singleton pattern
**Rationale**:
- O(1) lookup by ID
- O(n) iteration for list views
- Simple to implement
- Maintains insertion order in Python 3.7+

**Alternatives Considered**:
- List[Todo]: O(n) lookup by ID
- OrderedDict: Unnecessary since Python 3.7+
- External in-memory DB (sqlite :memory:): Violates minimal dependency principle

### 5. questionary Usage Patterns

**Decision**: Use `questionary.select()` for menus, `questionary.text()` for input, `questionary.confirm()` for deletions
**Rationale**:
- Clean, consistent API
- Built-in validation support
- Keyboard navigation for menus
- Matches FR-060 (interactive menu) and FR-041 (confirmation)

**Best Practices**:
```python
# Menu selection
action = questionary.select(
    "What would you like to do?",
    choices=["Add Todo", "View Todos", "Update Todo", "Delete Todo", "Toggle Complete", "Exit"]
).ask()

# Text input with validation
title = questionary.text(
    "Enter todo title:",
    validate=lambda x: len(x.strip()) > 0 or "Title cannot be empty"
).ask()

# Confirmation for destructive actions
if questionary.confirm("Are you sure you want to delete this todo?").ask():
    # proceed with deletion
```

### 6. rich Output Patterns

**Decision**: Use `rich.table.Table` for todo lists, `rich.console.Console.print()` for messages
**Rationale**:
- Beautiful, formatted output
- Built-in styling for completed items
- Cross-platform terminal support
- Matches FR-020 (formatted table) and FR-022 (visual distinction)

**Best Practices**:
```python
from rich.console import Console
from rich.table import Table

console = Console()

# Success message
console.print("[green]✓ Todo created successfully![/green]")

# Error message
console.print("[red]✗ Title cannot be empty[/red]")

# Todo table
table = Table(title="Your Todos")
table.add_column("ID", style="cyan")
table.add_column("Title")
table.add_column("Status", style="green")

for todo in todos:
    status = "✓ Complete" if todo.completed else "○ Pending"
    title_style = "strike" if todo.completed else ""
    table.add_row(str(todo.id), f"[{title_style}]{todo.title}[/{title_style}]", status)

console.print(table)
```

### 7. Error Handling Strategy

**Decision**: Use exceptions for validation errors, return None for "not found" cases
**Rationale**:
- Exceptions for truly exceptional conditions (invalid input)
- None/False returns for expected "not found" scenarios
- Clean separation between programming errors and user errors

**Patterns**:
```python
# Validation error (exception)
class ValidationError(Exception):
    pass

def validate_title(title: str) -> str:
    cleaned = title.strip()
    if not cleaned:
        raise ValidationError("Title cannot be empty")
    return cleaned

# Not found (return None)
def get_by_id(todo_id: int) -> Todo | None:
    return self._todos.get(todo_id)
```

### 8. Keyboard Interrupt Handling

**Decision**: Catch KeyboardInterrupt at main loop level, exit gracefully
**Rationale**:
- Prevents ugly stack traces for users
- Matches FR-064 (graceful interrupt handling)
- Simple to implement

**Pattern**:
```python
def main():
    try:
        while True:
            action = show_menu()
            handle_action(action)
            if action == "Exit":
                break
    except KeyboardInterrupt:
        console.print("\n[yellow]Goodbye![/yellow]")
```

## Technology Verification

### questionary Compatibility

- **Tested versions**: 2.0.0, 2.0.1 (both compatible)
- **Platform support**: Windows, macOS, Linux
- **Python support**: 3.8+
- **No known issues** for our use case

### rich Compatibility

- **Tested versions**: 13.0.0+ (all compatible)
- **Platform support**: Windows, macOS, Linux (with terminal detection)
- **Python support**: 3.7+
- **Fallback**: Degrades gracefully to plain text if terminal not supported

## Conclusion

All technical questions resolved. No NEEDS CLARIFICATION items remain. Ready for data model definition.
