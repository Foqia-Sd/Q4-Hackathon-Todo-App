"""Todo entity and related exceptions."""

from dataclasses import dataclass


class ValidationError(Exception):
    """Raised when input validation fails."""

    pass


class TodoNotFoundError(Exception):
    """Raised when a requested todo does not exist."""

    pass


@dataclass
class Todo:
    """Represents a single todo item.

    Attributes:
        id: Unique identifier (system-generated, immutable)
        title: User-provided description (required, non-empty string)
        completed: Completion status (default: False)
    """

    id: int
    title: str
    completed: bool = False

    def toggle(self) -> None:
        """Toggle completion status."""
        self.completed = not self.completed
