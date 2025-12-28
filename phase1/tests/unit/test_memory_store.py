"""Unit tests for MemoryStore."""

import pytest
from src.storage.memory_store import MemoryStore
from src.models.todo import Todo


class TestMemoryStore:
    """Tests for MemoryStore class."""

    def test_add_todo(self) -> None:
        """Test adding a todo assigns an ID and stores it."""
        store = MemoryStore()
        todo = store.add("Buy groceries")

        assert todo.id == 1
        assert todo.title == "Buy groceries"
        assert todo.completed is False

    def test_add_multiple_todos_unique_ids(self) -> None:
        """Test that multiple todos get unique IDs."""
        store = MemoryStore()
        todo1 = store.add("Task 1")
        todo2 = store.add("Task 2")
        todo3 = store.add("Task 3")

        assert todo1.id == 1
        assert todo2.id == 2
        assert todo3.id == 3

    def test_get_all_todos_empty(self) -> None:
        """Test get_all returns empty list when no todos."""
        store = MemoryStore()
        todos = store.get_all()

        assert todos == []

    def test_get_all_todos(self) -> None:
        """Test get_all returns all added todos."""
        store = MemoryStore()
        store.add("Task 1")
        store.add("Task 2")

        todos = store.get_all()

        assert len(todos) == 2
        assert todos[0].title == "Task 1"
        assert todos[1].title == "Task 2"

    def test_get_by_id_found(self) -> None:
        """Test get_by_id returns the correct todo."""
        store = MemoryStore()
        store.add("Task 1")
        todo2 = store.add("Task 2")

        result = store.get_by_id(2)

        assert result is not None
        assert result.id == todo2.id
        assert result.title == "Task 2"

    def test_get_by_id_not_found(self) -> None:
        """Test get_by_id returns None for non-existent ID."""
        store = MemoryStore()
        store.add("Task 1")

        result = store.get_by_id(999)

        assert result is None

    def test_update_todo(self) -> None:
        """Test updating a todo's title."""
        store = MemoryStore()
        store.add("Original title")

        result = store.update(1, "Updated title")

        assert result is not None
        assert result.title == "Updated title"

    def test_update_todo_not_found(self) -> None:
        """Test update returns None for non-existent ID."""
        store = MemoryStore()

        result = store.update(999, "New title")

        assert result is None

    def test_delete_todo(self) -> None:
        """Test deleting a todo."""
        store = MemoryStore()
        store.add("Task to delete")

        result = store.delete(1)

        assert result is True
        assert store.get_by_id(1) is None

    def test_delete_todo_not_found(self) -> None:
        """Test delete returns False for non-existent ID."""
        store = MemoryStore()

        result = store.delete(999)

        assert result is False

    def test_id_never_reused(self) -> None:
        """Test that IDs are never reused after deletion."""
        store = MemoryStore()
        store.add("Task 1")  # ID 1
        store.add("Task 2")  # ID 2
        store.delete(1)  # Delete ID 1
        todo3 = store.add("Task 3")  # Should get ID 3, not 1

        assert todo3.id == 3
        assert store.get_by_id(1) is None

    def test_count_empty(self) -> None:
        """Test count returns 0 for empty store."""
        store = MemoryStore()

        assert store.count() == 0

    def test_count_with_todos(self) -> None:
        """Test count returns correct number."""
        store = MemoryStore()
        store.add("Task 1")
        store.add("Task 2")

        assert store.count() == 2

    def test_is_empty_true(self) -> None:
        """Test is_empty returns True for empty store."""
        store = MemoryStore()

        assert store.is_empty() is True

    def test_is_empty_false(self) -> None:
        """Test is_empty returns False when todos exist."""
        store = MemoryStore()
        store.add("Task")

        assert store.is_empty() is False
