"""Operation handlers for CLI commands."""

import questionary

from src.models.todo import Todo, ValidationError
from src.services.todo_service import TodoService
from src.cli.display import (
    show_success,
    show_error,
    show_warning,
    show_todo_table,
    show_empty_list_message,
)


def handle_add_todo(service: TodoService) -> None:
    """Handle the Add Todo operation.

    Prompts user for a title, creates the todo, and displays confirmation.

    Args:
        service: The TodoService instance
    """
    try:
        title = questionary.text("Enter todo title:").ask()

        # User cancelled (Ctrl+C or escape)
        if title is None:
            show_warning("Cancelled")
            return

        todo = service.add_todo(title)
        show_success(f"Todo added: {todo.title} (ID: {todo.id})")

    except ValidationError as e:
        show_error(str(e))
    except KeyboardInterrupt:
        show_warning("Cancelled")


def handle_view_todos(service: TodoService) -> None:
    """Handle the View Todos operation.

    Displays all todos in a formatted table, or a message if empty.

    Args:
        service: The TodoService instance
    """
    todos = service.get_all_todos()

    if not todos:
        show_empty_list_message()
    else:
        show_todo_table(todos)


def select_todo(todos: list[Todo], prompt: str) -> Todo | None:
    """Present a selection list of todos and return the chosen one.

    Args:
        todos: List of Todo objects to choose from
        prompt: The prompt message to display

    Returns:
        The selected Todo object, or None if cancelled
    """
    if not todos:
        return None

    # Format choices with status indicator
    choices = []
    for todo in todos:
        status = "✓" if todo.completed else "○"
        choices.append(
            questionary.Choice(
                title=f"[{todo.id}] {status} {todo.title}",
                value=todo,
            )
        )

    selected = questionary.select(prompt, choices=choices).ask()
    return selected


def handle_toggle_complete(service: TodoService) -> None:
    """Handle the Toggle Complete operation.

    Prompts user to select a todo and toggles its completion status.

    Args:
        service: The TodoService instance
    """
    todos = service.get_all_todos()

    if not todos:
        show_warning("No todos to toggle")
        return

    try:
        todo = select_todo(todos, "Select a todo to toggle:")

        if todo is None:
            show_warning("Cancelled")
            return

        updated = service.toggle_complete(todo.id)

        if updated.completed:
            show_success(f"Marked complete: {updated.title}")
        else:
            show_warning(f"○ Marked incomplete: {updated.title}")

    except KeyboardInterrupt:
        show_warning("Cancelled")


def handle_update_todo(service: TodoService) -> None:
    """Handle the Update Todo operation.

    Prompts user to select a todo and enter a new title.

    Args:
        service: The TodoService instance
    """
    todos = service.get_all_todos()

    if not todos:
        show_warning("No todos to update")
        return

    try:
        todo = select_todo(todos, "Select a todo to update:")

        if todo is None:
            show_warning("Cancelled")
            return

        old_title = todo.title
        new_title = questionary.text(
            "Enter new title:", default=old_title
        ).ask()

        if new_title is None:
            show_warning("Cancelled")
            return

        updated = service.update_todo(todo.id, new_title)
        show_success(f"Todo updated: {old_title} → {updated.title}")

    except ValidationError as e:
        show_error(str(e))
    except KeyboardInterrupt:
        show_warning("Cancelled")


def handle_delete_todo(service: TodoService) -> None:
    """Handle the Delete Todo operation.

    Prompts user to select a todo and confirm deletion.

    Args:
        service: The TodoService instance
    """
    todos = service.get_all_todos()

    if not todos:
        show_warning("No todos to delete")
        return

    try:
        todo = select_todo(todos, "Select a todo to delete:")

        if todo is None:
            show_warning("Cancelled")
            return

        confirm = questionary.confirm(
            f"Are you sure you want to delete '{todo.title}'?",
            default=False,
        ).ask()

        if confirm is None or not confirm:
            show_warning("Deletion cancelled")
            return

        service.delete_todo(todo.id)
        show_success(f"Todo deleted: {todo.title}")

    except KeyboardInterrupt:
        show_warning("Cancelled")
