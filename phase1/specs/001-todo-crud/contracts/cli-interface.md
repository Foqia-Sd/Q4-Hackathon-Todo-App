# CLI Interface Contract: User Interaction Layer

**Branch**: `001-todo-crud` | **Date**: 2025-12-27
**Purpose**: Define the CLI user interface behavior and messaging

## Overview

This contract defines the exact user-facing behavior of the CLI, including menu options, prompts, and output messages.

## Main Menu

### Menu Structure

```
╭─────────────────────────────────────────╮
│          Todo Manager                    │
│                                          │
│  What would you like to do?             │
│                                          │
│  > Add Todo                             │
│    View Todos                           │
│    Update Todo                          │
│    Delete Todo                          │
│    Toggle Complete                      │
│    Exit                                 │
╰─────────────────────────────────────────╯
```

### Menu Options

| Option | Action Key | Description |
|--------|------------|-------------|
| Add Todo | `add` | Create a new todo item |
| View Todos | `view` | Display all todos in table |
| Update Todo | `update` | Modify an existing todo's title |
| Delete Todo | `delete` | Remove a todo (with confirmation) |
| Toggle Complete | `toggle` | Mark todo complete/incomplete |
| Exit | `exit` | Close the application |

## Operation: Add Todo

### Flow

```
1. User selects "Add Todo"
2. Prompt: "Enter todo title: "
3a. If valid title:
    - Display: "✓ Todo added: [title] (ID: [id])"
    - Return to main menu
3b. If empty title:
    - Display: "✗ Title cannot be empty"
    - Re-prompt for title
3c. If user cancels (Ctrl+C or escape):
    - Display: "Cancelled"
    - Return to main menu
```

### Messages

| Condition | Message |
|-----------|---------|
| Success | `✓ Todo added: {title} (ID: {id})` |
| Empty title | `✗ Title cannot be empty` |
| Cancelled | `Cancelled` |

---

## Operation: View Todos

### Flow

```
1. User selects "View Todos"
2a. If todos exist:
    - Display formatted table with all todos
    - Return to main menu
2b. If no todos:
    - Display: "No todos yet. Add one to get started!"
    - Return to main menu
```

### Table Format

```
┏━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┓
┃ ID ┃ Title                  ┃ Status      ┃
┡━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━┩
│  1 │ Buy groceries          │ ○ Pending   │
│  2 │ Walk the dog           │ ✓ Complete  │
│  3 │ Finish report          │ ○ Pending   │
└────┴────────────────────────┴─────────────┘
```

### Styling

| Element | Style |
|---------|-------|
| ID column | Cyan text |
| Completed title | Strikethrough |
| Pending status | Default text, "○ Pending" |
| Complete status | Green text, "✓ Complete" |

### Messages

| Condition | Message |
|-----------|---------|
| Empty list | `No todos yet. Add one to get started!` |

---

## Operation: Update Todo

### Flow

```
1. User selects "Update Todo"
2a. If no todos:
    - Display: "No todos to update"
    - Return to main menu
2b. If todos exist:
    - Display todo selection list
    - Prompt: "Select a todo to update: "
3. User selects a todo
4. Prompt: "Enter new title: "
5a. If valid title:
    - Display: "✓ Todo updated: [old_title] → [new_title]"
    - Return to main menu
5b. If empty title:
    - Display: "✗ Title cannot be empty"
    - Re-prompt for title
5c. If user cancels:
    - Display: "Cancelled"
    - Return to main menu
```

### Todo Selection Format

```
Select a todo to update:
> [1] Buy groceries
  [2] Walk the dog
  [3] Finish report
```

### Messages

| Condition | Message |
|-----------|---------|
| No todos | `No todos to update` |
| Success | `✓ Todo updated: {old_title} → {new_title}` |
| Empty title | `✗ Title cannot be empty` |
| Cancelled | `Cancelled` |

---

## Operation: Delete Todo

### Flow

```
1. User selects "Delete Todo"
2a. If no todos:
    - Display: "No todos to delete"
    - Return to main menu
2b. If todos exist:
    - Display todo selection list
    - Prompt: "Select a todo to delete: "
3. User selects a todo
4. Prompt: "Are you sure you want to delete '[title]'? (y/N): "
5a. If confirmed (y/yes):
    - Display: "✓ Todo deleted: [title]"
    - Return to main menu
5b. If declined (n/no/enter):
    - Display: "Deletion cancelled"
    - Return to main menu
```

### Messages

| Condition | Message |
|-----------|---------|
| No todos | `No todos to delete` |
| Confirm prompt | `Are you sure you want to delete '{title}'? (y/N)` |
| Success | `✓ Todo deleted: {title}` |
| Cancelled | `Deletion cancelled` |

---

## Operation: Toggle Complete

### Flow

```
1. User selects "Toggle Complete"
2a. If no todos:
    - Display: "No todos to toggle"
    - Return to main menu
2b. If todos exist:
    - Display todo selection list with current status
    - Prompt: "Select a todo to toggle: "
3. User selects a todo
4a. If was incomplete:
    - Mark as complete
    - Display: "✓ Marked complete: [title]"
4b. If was complete:
    - Mark as incomplete
    - Display: "○ Marked incomplete: [title]"
5. Return to main menu
```

### Todo Selection Format (with status)

```
Select a todo to toggle:
> [1] ○ Buy groceries
  [2] ✓ Walk the dog
  [3] ○ Finish report
```

### Messages

| Condition | Message |
|-----------|---------|
| No todos | `No todos to toggle` |
| Marked complete | `✓ Marked complete: {title}` |
| Marked incomplete | `○ Marked incomplete: {title}` |

---

## Operation: Exit

### Flow

```
1. User selects "Exit"
2. Display: "Goodbye! Your todos have not been saved."
3. Application terminates
```

### Messages

| Condition | Message |
|-----------|---------|
| Exit | `Goodbye! Your todos have not been saved.` |

---

## Keyboard Interrupt Handling

### Flow

```
1. User presses Ctrl+C at any point
2. Display: "Goodbye!"
3. Application terminates gracefully
```

### Messages

| Condition | Message |
|-----------|---------|
| Interrupt | `Goodbye!` |

---

## Color Scheme

| Element | Color |
|---------|-------|
| Success messages | Green |
| Error messages | Red |
| Warning messages | Yellow |
| ID values | Cyan |
| Completed items | Green with strikethrough |
| Menu title | Bold |
| Prompts | Default |

## Contract Validation

| Contract | Spec Requirement | Verified |
|----------|------------------|----------|
| Main menu displays all options | FR-060 | ✓ |
| Returns to menu after operation | FR-061 | ✓ |
| Exit option exists | FR-062 | ✓ |
| Goodbye message on exit | FR-063 | ✓ |
| Keyboard interrupt handled | FR-064 | ✓ |
| Success confirmation for add | FR-014 | ✓ |
| Empty list message | FR-023 | ✓ |
| Success confirmation for update | FR-033 | ✓ |
| Delete confirmation required | FR-041 | ✓ |
| Success confirmation for delete | FR-044 | ✓ |
| Toggle confirmation | FR-053 | ✓ |
