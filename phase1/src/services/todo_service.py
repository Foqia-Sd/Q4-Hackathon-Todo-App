"""Business logic layer for todo operations."""

from src.models.todo import Todo, ValidationError, TodoNotFoundError
from src.storage.memory_store import MemoryStore


class TodoService:
    """Service class for todo operations.

    Handles validation, business rules, and delegates
    storage operations to the MemoryStore.
    """

    def __init__(self, store: MemoryStore | None = None) -> None:
        """Initialize service with optional store injection.

        Args:
            store: Optional MemoryStore instance. Creates new one if not provided.
        """
        self._store = store if store is not None else MemoryStore()

    def validate_title(self, title: str) -> str:
        """Validate and normalize a todo title.

        Args:
            title: The title to validate

        Returns:
            Cleaned title (stripped of whitespace)

        Raises:
            ValidationError: If title is empty or whitespace-only
        """
        cleaned = title.strip()
        if not cleaned:
            raise ValidationError("Title cannot be empty")
        return cleaned

    def add_todo(self, title: str) -> Todo:
        """Create a new todo with the given title.

        Args:
            title: The todo title (must be non-empty after trimming)

        Returns:
            The created Todo object with assigned ID

        Raises:
            ValidationError: If title is empty or whitespace-only
        """
        cleaned_title = self.validate_title(title)
        return self._store.add(cleaned_title)

    def get_all_todos(self) -> list[Todo]:
        """Get all todos.

        Returns:
            List of all Todo objects (may be empty)
        """
        return self._store.get_all()

    def get_todo_by_id(self, todo_id: int) -> Todo | None:
        """Get a todo by its ID.

        Args:
            todo_id: The ID of the todo to retrieve

        Returns:
            The Todo object if found, None otherwise
        """
        return self._store.get_by_id(todo_id)

    def update_todo(self, todo_id: int, new_title: str) -> Todo:
        """Update a todo's title.

        Args:
            todo_id: The ID of the todo to update
            new_title: The new title (must be non-empty after trimming)

        Returns:
            The updated Todo object

        Raises:
            ValidationError: If new_title is empty or whitespace-only
            TodoNotFoundError: If todo with given ID does not exist
        """
        cleaned_title = self.validate_title(new_title)
        todo = self._store.update(todo_id, cleaned_title)
        if todo is None:
            raise TodoNotFoundError("Todo not found")
        return todo

    def delete_todo(self, todo_id: int) -> bool:
        """Delete a todo by its ID.

        Args:
            todo_id: The ID of the todo to delete

        Returns:
            True if deleted, False if not found
        """
        return self._store.delete(todo_id)

    def toggle_complete(self, todo_id: int) -> Todo:
        """Toggle a todo's completion status.

        Args:
            todo_id: The ID of the todo to toggle

        Returns:
            The updated Todo object

        Raises:
            TodoNotFoundError: If todo with given ID does not exist
        """
        todo = self._store.get_by_id(todo_id)
        if todo is None:
            raise TodoNotFoundError("Todo not found")
        todo.toggle()
        return todo

    def has_todos(self) -> bool:
        """Check if there are any todos.

        Returns:
            True if at least one todo exists, False otherwise
        """
        return not self._store.is_empty()
