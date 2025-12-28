# Quickstart: Phase 1 In-Memory Todo Application

**Branch**: `001-todo-crud` | **Date**: 2025-12-27
**Purpose**: Get the application running and verify all features work

## Prerequisites

- Python 3.11 or higher
- uv package manager installed

## Installation

### 1. Clone and Navigate

```bash
cd phase1
```

### 2. Install Dependencies

```bash
# Using uv (required by constitution)
uv sync
```

Or if setting up fresh:

```bash
uv init --name todo-app
uv add questionary rich
uv add --dev pytest pytest-cov
```

## Running the Application

```bash
# Run the application
uv run python -m src.main
```

Or:

```bash
# Activate virtual environment first
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# Then run
python -m src.main
```

## Feature Verification Checklist

### Setup Verification

- [ ] Application starts without errors
- [ ] Main menu displays all 6 options
- [ ] Menu can be navigated with arrow keys

### Add Todo (P1)

- [ ] Select "Add Todo" from menu
- [ ] Enter "Buy groceries" as title
- [ ] Verify success message: "✓ Todo added: Buy groceries (ID: 1)"
- [ ] Returns to main menu automatically

**Edge Case Tests**:
- [ ] Try adding with empty title → Error message appears
- [ ] Try adding with spaces only → Error message appears
- [ ] Add todo with special characters (quotes, unicode) → Works correctly

### View Todos (P1)

- [ ] Select "View Todos" from menu
- [ ] Table displays with columns: ID, Title, Status
- [ ] Added todo appears in the list
- [ ] Status shows "○ Pending" for new todos

**Edge Case Tests**:
- [ ] View with no todos → "No todos yet" message
- [ ] View with many todos → All display correctly

### Toggle Complete (P2)

- [ ] Select "Toggle Complete" from menu
- [ ] Select "Buy groceries" todo
- [ ] Verify: "✓ Marked complete: Buy groceries"
- [ ] View todos → Status shows "✓ Complete"
- [ ] Toggle again → "○ Marked incomplete: Buy groceries"

**Edge Case Tests**:
- [ ] Toggle with no todos → "No todos to toggle" message

### Update Todo (P3)

- [ ] Select "Update Todo" from menu
- [ ] Select "Buy groceries" todo
- [ ] Enter "Buy organic groceries"
- [ ] Verify: "✓ Todo updated: Buy groceries → Buy organic groceries"
- [ ] View todos → Title is updated

**Edge Case Tests**:
- [ ] Update with empty title → Error, original preserved
- [ ] Update with no todos → "No todos to update" message

### Delete Todo (P3)

- [ ] Add a test todo: "Delete me"
- [ ] Select "Delete Todo" from menu
- [ ] Select "Delete me" todo
- [ ] Confirm deletion → "✓ Todo deleted: Delete me"
- [ ] View todos → Todo is gone

**Edge Case Tests**:
- [ ] Decline deletion → Todo preserved
- [ ] Delete with no todos → "No todos to delete" message

### Exit (P1)

- [ ] Select "Exit" from menu
- [ ] Verify: "Goodbye! Your todos have not been saved."
- [ ] Application terminates cleanly

**Edge Case Tests**:
- [ ] Press Ctrl+C at any point → Graceful exit
- [ ] Exit with todos → No crash (data expected to be lost)

## Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-report=term-missing

# Run specific test file
uv run pytest tests/unit/test_todo.py -v
```

## Expected Test Results

```
tests/unit/test_todo.py::test_todo_creation PASSED
tests/unit/test_todo.py::test_todo_toggle PASSED
tests/unit/test_todo_service.py::test_add_todo PASSED
tests/unit/test_todo_service.py::test_add_todo_empty_title PASSED
tests/unit/test_todo_service.py::test_get_all_todos PASSED
tests/unit/test_todo_service.py::test_update_todo PASSED
tests/unit/test_todo_service.py::test_delete_todo PASSED
tests/unit/test_todo_service.py::test_toggle_complete PASSED
```

## Troubleshooting

### "Module not found" error

```bash
# Ensure you're in the project root
cd phase1

# Reinstall dependencies
uv sync
```

### "questionary not working" on Windows

Some Windows terminals don't support ANSI. Try:
- Use Windows Terminal (recommended)
- Use Git Bash
- Use VSCode integrated terminal

### "rich not displaying colors"

```bash
# Force color output
export TERM=xterm-256color  # Linux/macOS
set TERM=xterm-256color     # Windows CMD
```

## Success Criteria Verification

| Criteria | How to Verify | Expected |
|----------|---------------|----------|
| SC-001 | Time add operation | < 10 seconds |
| SC-002 | Time view operation | < 2 seconds |
| SC-003 | Time toggle operation | < 5 seconds |
| SC-004 | Time update operation | < 15 seconds |
| SC-005 | Time delete operation | < 10 seconds |
| SC-006 | Try all invalid inputs | Error messages, no crashes |
| SC-007 | Select Exit | Clean termination |
| SC-008 | Complete any operation | Returns to menu |

## Demo Script

For a quick demonstration:

```
1. Start app
2. Add: "Write documentation"
3. Add: "Review code"
4. Add: "Deploy to production"
5. View todos (show table with 3 items)
6. Toggle #1 complete
7. View todos (show #1 as complete)
8. Update #2 to "Review and approve code"
9. View todos (show updated title)
10. Delete #3 (confirm)
11. View todos (only 2 remaining)
12. Exit
```

Total demo time: ~2 minutes
