"""In-memory storage for todos."""

from src.models.todo import Todo


class MemoryStore:
    """In-memory storage for todos.

    Stores todos in a dictionary with auto-incrementing IDs.
    IDs are never reused, even after deletion.
    """

    def __init__(self) -> None:
        """Initialize empty store with ID counter starting at 1."""
        self._todos: dict[int, Todo] = {}
        self._next_id: int = 1

    def add(self, title: str) -> Todo:
        """Add a new todo and return it with assigned ID.

        Args:
            title: The todo title (assumed pre-validated)

        Returns:
            The created Todo object with assigned ID
        """
        todo = Todo(id=self._next_id, title=title)
        self._todos[self._next_id] = todo
        self._next_id += 1
        return todo

    def get_all(self) -> list[Todo]:
        """Return all todos in insertion order.

        Returns:
            List of all Todo objects (may be empty)
        """
        return list(self._todos.values())

    def get_by_id(self, todo_id: int) -> Todo | None:
        """Return todo by ID or None if not found.

        Args:
            todo_id: The ID of the todo to retrieve

        Returns:
            The Todo object if found, None otherwise
        """
        return self._todos.get(todo_id)

    def update(self, todo_id: int, title: str) -> Todo | None:
        """Update todo title, return updated todo or None.

        Args:
            todo_id: The ID of the todo to update
            title: The new title (assumed pre-validated)

        Returns:
            The updated Todo object if found, None otherwise
        """
        todo = self._todos.get(todo_id)
        if todo:
            todo.title = title
        return todo

    def delete(self, todo_id: int) -> bool:
        """Delete todo by ID, return True if deleted.

        Args:
            todo_id: The ID of the todo to delete

        Returns:
            True if todo was deleted, False if not found
        """
        if todo_id in self._todos:
            del self._todos[todo_id]
            return True
        return False

    def count(self) -> int:
        """Return number of todos.

        Returns:
            The count of todos in the store
        """
        return len(self._todos)

    def is_empty(self) -> bool:
        """Return True if no todos exist.

        Returns:
            True if store is empty, False otherwise
        """
        return len(self._todos) == 0
