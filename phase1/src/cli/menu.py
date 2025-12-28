"""Main menu and navigation."""

import questionary
from rich.console import Console

console = Console()

# Menu choices mapping display text to action keys
MENU_CHOICES = [
    questionary.Choice(title="Add Todo", value="add"),
    questionary.Choice(title="View Todos", value="view"),
    questionary.Choice(title="Toggle Complete", value="toggle"),
    questionary.Choice(title="Update Todo", value="update"),
    questionary.Choice(title="Delete Todo", value="delete"),
    questionary.Choice(title="Exit", value="exit"),
]


def show_menu() -> str | None:
    """Display the main menu and return the selected action.

    Returns:
        The action key ('add', 'view', 'toggle', 'update', 'delete', 'exit')
        or None if cancelled.
    """
    console.print("\n[bold]Todo Manager[/bold]")

    action = questionary.select(
        "What would you like to do?",
        choices=MENU_CHOICES,
    ).ask()

    return action
