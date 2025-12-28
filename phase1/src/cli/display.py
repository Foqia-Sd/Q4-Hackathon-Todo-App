"""Rich output formatting for the CLI."""

from rich.console import Console
from rich.table import Table

from src.models.todo import Todo

# Shared console instance
console = Console()


def show_success(message: str) -> None:
    """Display a success message in green.

    Args:
        message: The message to display
    """
    console.print(f"[green]✓ {message}[/green]")


def show_error(message: str) -> None:
    """Display an error message in red.

    Args:
        message: The message to display
    """
    console.print(f"[red]✗ {message}[/red]")


def show_warning(message: str) -> None:
    """Display a warning message in yellow.

    Args:
        message: The message to display
    """
    console.print(f"[yellow]{message}[/yellow]")


def show_todo_table(todos: list[Todo]) -> None:
    """Display todos in a formatted table.

    Args:
        todos: List of Todo objects to display
    """
    table = Table(title="Your Todos")
    table.add_column("ID", style="cyan", justify="right")
    table.add_column("Title")
    table.add_column("Status")

    for todo in todos:
        if todo.completed:
            status = "[green]✓ Complete[/green]"
            title_display = f"[strike]{todo.title}[/strike]"
        else:
            status = "○ Pending"
            title_display = todo.title

        table.add_row(str(todo.id), title_display, status)

    console.print(table)


def show_empty_list_message() -> None:
    """Display a friendly message when no todos exist."""
    console.print("[dim]No todos yet. Add one to get started![/dim]")


def show_goodbye() -> None:
    """Display goodbye message with warning about unsaved data."""
    console.print("[yellow]Goodbye! Your todos have not been saved.[/yellow]")
