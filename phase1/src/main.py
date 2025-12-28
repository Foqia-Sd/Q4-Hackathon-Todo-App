"""Application entry point."""

from src.services.todo_service import TodoService
from src.cli.menu import show_menu
from src.cli.display import show_goodbye, console
from src.cli.handlers import (
    handle_add_todo,
    handle_view_todos,
    handle_toggle_complete,
    handle_update_todo,
    handle_delete_todo,
)


def main() -> None:
    """Main application loop.

    Initializes the service, displays the menu, and routes
    user actions to the appropriate handlers.
    """
    service = TodoService()

    try:
        while True:
            action = show_menu()

            # User cancelled menu (Ctrl+C or escape)
            if action is None:
                show_goodbye()
                break

            if action == "add":
                handle_add_todo(service)
            elif action == "view":
                handle_view_todos(service)
            elif action == "toggle":
                handle_toggle_complete(service)
            elif action == "update":
                handle_update_todo(service)
            elif action == "delete":
                handle_delete_todo(service)
            elif action == "exit":
                show_goodbye()
                break

    except KeyboardInterrupt:
        console.print("\n[yellow]Goodbye![/yellow]")


if __name__ == "__main__":
    main()
