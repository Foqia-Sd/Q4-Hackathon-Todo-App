"""Unit tests for TodoService."""

import pytest
from src.services.todo_service import TodoService
from src.models.todo import ValidationError, TodoNotFoundError


class TestTodoService:
    """Tests for TodoService class."""

    def test_add_todo_success(self) -> None:
        """Test adding a todo with valid title."""
        service = TodoService()
        todo = service.add_todo("Buy groceries")

        assert todo.id == 1
        assert todo.title == "Buy groceries"
        assert todo.completed is False

    def test_add_todo_strips_whitespace(self) -> None:
        """Test that title whitespace is stripped."""
        service = TodoService()
        todo = service.add_todo("  Buy groceries  ")

        assert todo.title == "Buy groceries"

    def test_add_todo_empty_title(self) -> None:
        """Test that empty title raises ValidationError."""
        service = TodoService()

        with pytest.raises(ValidationError) as exc_info:
            service.add_todo("")

        assert "Title cannot be empty" in str(exc_info.value)

    def test_add_todo_whitespace_only_title(self) -> None:
        """Test that whitespace-only title raises ValidationError."""
        service = TodoService()

        with pytest.raises(ValidationError) as exc_info:
            service.add_todo("   ")

        assert "Title cannot be empty" in str(exc_info.value)

    def test_get_all_todos_empty(self) -> None:
        """Test get_all_todos returns empty list when none exist."""
        service = TodoService()

        todos = service.get_all_todos()

        assert todos == []

    def test_get_all_todos(self) -> None:
        """Test get_all_todos returns all todos."""
        service = TodoService()
        service.add_todo("Task 1")
        service.add_todo("Task 2")

        todos = service.get_all_todos()

        assert len(todos) == 2

    def test_get_todo_by_id_found(self) -> None:
        """Test get_todo_by_id returns correct todo."""
        service = TodoService()
        created = service.add_todo("Test task")

        found = service.get_todo_by_id(created.id)

        assert found is not None
        assert found.title == "Test task"

    def test_get_todo_by_id_not_found(self) -> None:
        """Test get_todo_by_id returns None for non-existent ID."""
        service = TodoService()

        found = service.get_todo_by_id(999)

        assert found is None

    def test_update_todo_success(self) -> None:
        """Test updating a todo's title."""
        service = TodoService()
        todo = service.add_todo("Original")

        updated = service.update_todo(todo.id, "Updated")

        assert updated.title == "Updated"

    def test_update_todo_empty_title(self) -> None:
        """Test update with empty title raises ValidationError."""
        service = TodoService()
        todo = service.add_todo("Original")

        with pytest.raises(ValidationError):
            service.update_todo(todo.id, "")

    def test_update_todo_not_found(self) -> None:
        """Test update non-existent todo raises TodoNotFoundError."""
        service = TodoService()

        with pytest.raises(TodoNotFoundError):
            service.update_todo(999, "New title")

    def test_delete_todo_success(self) -> None:
        """Test deleting a todo."""
        service = TodoService()
        todo = service.add_todo("To delete")

        result = service.delete_todo(todo.id)

        assert result is True
        assert service.get_todo_by_id(todo.id) is None

    def test_delete_todo_not_found(self) -> None:
        """Test deleting non-existent todo returns False."""
        service = TodoService()

        result = service.delete_todo(999)

        assert result is False

    def test_toggle_complete_incomplete_to_complete(self) -> None:
        """Test toggling incomplete todo to complete."""
        service = TodoService()
        todo = service.add_todo("Task")
        assert todo.completed is False

        toggled = service.toggle_complete(todo.id)

        assert toggled.completed is True

    def test_toggle_complete_complete_to_incomplete(self) -> None:
        """Test toggling complete todo back to incomplete."""
        service = TodoService()
        todo = service.add_todo("Task")
        service.toggle_complete(todo.id)  # Make complete

        toggled = service.toggle_complete(todo.id)

        assert toggled.completed is False

    def test_toggle_complete_not_found(self) -> None:
        """Test toggling non-existent todo raises TodoNotFoundError."""
        service = TodoService()

        with pytest.raises(TodoNotFoundError):
            service.toggle_complete(999)

    def test_has_todos_false_when_empty(self) -> None:
        """Test has_todos returns False when no todos."""
        service = TodoService()

        assert service.has_todos() is False

    def test_has_todos_true_when_todos_exist(self) -> None:
        """Test has_todos returns True when todos exist."""
        service = TodoService()
        service.add_todo("Task")

        assert service.has_todos() is True

    def test_validate_title_success(self) -> None:
        """Test validate_title returns cleaned title."""
        service = TodoService()

        result = service.validate_title("  Valid title  ")

        assert result == "Valid title"

    def test_validate_title_empty(self) -> None:
        """Test validate_title raises for empty title."""
        service = TodoService()

        with pytest.raises(ValidationError):
            service.validate_title("")
