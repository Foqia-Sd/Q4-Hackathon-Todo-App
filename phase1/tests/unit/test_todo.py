"""Unit tests for Todo model."""

import pytest
from src.models.todo import Todo, ValidationError, TodoNotFoundError


class TestTodo:
    """Tests for Todo dataclass."""

    def test_todo_creation(self) -> None:
        """Test that a todo can be created with required fields."""
        todo = Todo(id=1, title="Buy groceries")
        assert todo.id == 1
        assert todo.title == "Buy groceries"
        assert todo.completed is False

    def test_todo_creation_with_completed(self) -> None:
        """Test that a todo can be created with completed=True."""
        todo = Todo(id=1, title="Done task", completed=True)
        assert todo.completed is True

    def test_todo_default_incomplete(self) -> None:
        """Test that todos are incomplete by default."""
        todo = Todo(id=1, title="New task")
        assert todo.completed is False

    def test_todo_toggle_incomplete_to_complete(self) -> None:
        """Test toggling an incomplete todo to complete."""
        todo = Todo(id=1, title="Task")
        assert todo.completed is False
        todo.toggle()
        assert todo.completed is True

    def test_todo_toggle_complete_to_incomplete(self) -> None:
        """Test toggling a complete todo back to incomplete."""
        todo = Todo(id=1, title="Task", completed=True)
        assert todo.completed is True
        todo.toggle()
        assert todo.completed is False

    def test_todo_toggle_multiple_times(self) -> None:
        """Test toggling multiple times."""
        todo = Todo(id=1, title="Task")
        todo.toggle()  # False -> True
        todo.toggle()  # True -> False
        todo.toggle()  # False -> True
        assert todo.completed is True


class TestExceptions:
    """Tests for custom exceptions."""

    def test_validation_error_exists(self) -> None:
        """Test that ValidationError can be raised."""
        with pytest.raises(ValidationError):
            raise ValidationError("Title cannot be empty")

    def test_todo_not_found_error_exists(self) -> None:
        """Test that TodoNotFoundError can be raised."""
        with pytest.raises(TodoNotFoundError):
            raise TodoNotFoundError("Todo not found")
