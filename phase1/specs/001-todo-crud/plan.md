# Implementation Plan: Phase 1 In-Memory Todo CRUD Application

**Branch**: `001-todo-crud` | **Date**: 2025-12-27 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-todo-crud/spec.md`
**Constitution**: `.specify/memory/constitution.md` v1.0.0

## Summary

Build a Python console application for managing todo items entirely in memory. The application provides complete CRUD operations (Create, Read, Update, Delete) plus completion status toggling through an interactive CLI. Architecture follows a clean 3-layer separation: CLI Interaction Layer (questionary/rich), Application Logic Layer (todo operations), and Data Storage Layer (in-memory state).

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: questionary (CLI prompts), rich (formatted output)
**Package Manager**: uv (mandatory per constitution)
**Storage**: In-memory only (Python list/dict)
**Testing**: pytest (standard Python testing)
**Target Platform**: Cross-platform console (Windows, macOS, Linux)
**Project Type**: Single project
**Performance Goals**: Instant response (<100ms for all operations)
**Constraints**: No file I/O for data, single-user, session-scoped data
**Scale/Scope**: Single user, unlimited todos per session (memory-bound only)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Requirement | Status | Notes |
|-----------|-------------|--------|-------|
| I. Spec-Driven Development | Spec exists before plan | ✅ PASS | spec.md completed and validated |
| II. Reusable Intelligence | Produces reusable artifacts | ✅ PASS | Plan creates reusable patterns |
| III. In-Memory Simplicity | No persistence, single-user | ✅ PASS | In-memory storage only |
| IV. Minimal Dependencies | Only uv, rich, questionary | ✅ PASS | No additional dependencies |
| V. Todo Entity Contract | ID, Title, Completed only | ✅ PASS | Matches spec FR-001 to FR-005 |
| VI. Complete CRUD Operations | All operations supported | ✅ PASS | All 5 operations in spec |
| VII. Clean CLI Experience | questionary + rich UX | ✅ PASS | Architecture supports this |

**Gate Result**: ✅ ALL PRINCIPLES PASS - Proceed to Phase 0

## Project Structure

### Documentation (this feature)

```text
specs/001-todo-crud/
├── spec.md              # Feature specification (completed)
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── checklists/          # Validation checklists
│   └── requirements.md  # Spec quality checklist (completed)
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
src/
├── __init__.py
├── main.py              # Application entry point
├── models/
│   ├── __init__.py
│   └── todo.py          # Todo entity class
├── services/
│   ├── __init__.py
│   └── todo_service.py  # Business logic layer
├── storage/
│   ├── __init__.py
│   └── memory_store.py  # In-memory data storage
└── cli/
    ├── __init__.py
    ├── menu.py          # Main menu and navigation
    ├── handlers.py      # Operation handlers
    └── display.py       # Rich output formatting

tests/
├── __init__.py
├── unit/
│   ├── __init__.py
│   ├── test_todo.py
│   └── test_todo_service.py
└── integration/
    ├── __init__.py
    └── test_cli_flows.py

pyproject.toml           # uv project configuration
```

**Structure Decision**: Single project structure with clear layer separation:
- `src/models/` - Data entities (Todo)
- `src/services/` - Business logic (TodoService)
- `src/storage/` - Data access layer (MemoryStore)
- `src/cli/` - User interface layer (menus, handlers, display)

## Architecture

### Layer Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    CLI Interaction Layer                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   menu.py   │  │ handlers.py │  │     display.py      │  │
│  │ (questionary│  │  (operation │  │   (rich tables,     │  │
│  │   menus)    │  │   routing)  │  │    messages)        │  │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘  │
└─────────┼────────────────┼─────────────────────┼────────────┘
          │                │                     │
          ▼                ▼                     │
┌─────────────────────────────────────────────────────────────┐
│                  Application Logic Layer                     │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                   todo_service.py                     │   │
│  │  • add_todo(title) → Todo                            │   │
│  │  • get_all_todos() → List[Todo]                      │   │
│  │  • update_todo(id, title) → Todo                     │   │
│  │  • delete_todo(id) → bool                            │   │
│  │  • toggle_complete(id) → Todo                        │   │
│  │  • validate_title(title) → bool                      │   │
│  └──────────────────────────┬───────────────────────────┘   │
└─────────────────────────────┼───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Data Storage Layer                        │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                  memory_store.py                      │   │
│  │  • _todos: Dict[int, Todo]  (private storage)        │   │
│  │  • _next_id: int            (ID generator)           │   │
│  │  • add(todo) → int                                   │   │
│  │  • get_all() → List[Todo]                            │   │
│  │  • get_by_id(id) → Todo | None                       │   │
│  │  • update(id, todo) → bool                           │   │
│  │  • delete(id) → bool                                 │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Layer Responsibilities

| Layer | Files | Responsibility | Dependencies |
|-------|-------|----------------|--------------|
| CLI Interaction | `cli/*.py` | User input/output, menu navigation | questionary, rich |
| Application Logic | `services/todo_service.py` | Business rules, validation | models, storage |
| Data Storage | `storage/memory_store.py` | In-memory CRUD operations | models |
| Models | `models/todo.py` | Data structures | None |

### Data Flow Example: Add Todo

```
1. User selects "Add Todo" from menu
   └─► menu.py: questionary.select() returns "add"

2. Handler routes to add operation
   └─► handlers.py: handle_add_todo()

3. Prompt for title input
   └─► questionary.text("Enter todo title:")

4. Validate and create todo
   └─► todo_service.add_todo(title)
       └─► validate_title(title)  # Check non-empty
       └─► memory_store.add(Todo(title=title))
           └─► Assign ID, store in dict

5. Display confirmation
   └─► display.py: show_success("Todo created!")
   └─► Return to main menu
```

## Complexity Tracking

No constitution violations detected. Architecture follows minimal complexity principles:

- Single project structure (no unnecessary separation)
- No external database (in-memory only)
- No API layer (console-only)
- Three logical layers with clear boundaries
- No design patterns beyond basic service layer

## Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| ID Generation | Auto-incrementing integer | Simple, predictable, matches spec assumptions |
| Storage Structure | Dict[int, Todo] | O(1) lookup by ID, preserves insertion order in Python 3.7+ |
| Title Validation | Service layer | Centralized validation before storage operations |
| Error Handling | Return values + exceptions | Use None/False for "not found", exceptions for validation |
| Menu Loop | While loop in main | Simple, explicit control flow |

## Dependencies

### Runtime Dependencies

```toml
[project]
dependencies = [
    "questionary>=2.0.0",
    "rich>=13.0.0",
]
```

### Development Dependencies

```toml
[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-cov>=4.0.0",
]
```

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| questionary incompatibility | Low | High | Pin version, test on target platforms |
| rich rendering issues | Low | Medium | Use basic formatting as fallback |
| Large todo list performance | Low | Low | In-memory dict is fast; session-scoped limits growth |
| Keyboard interrupt handling | Medium | Low | Wrap main loop in try/except KeyboardInterrupt |

## Post-Design Constitution Re-Check

| Principle | Status | Verification |
|-----------|--------|--------------|
| I. Spec-Driven | ✅ PASS | Plan follows spec requirements exactly |
| II. Reusable Intelligence | ✅ PASS | Layer patterns reusable for future phases |
| III. In-Memory Simplicity | ✅ PASS | No persistence in design |
| IV. Minimal Dependencies | ✅ PASS | Only questionary + rich |
| V. Todo Entity Contract | ✅ PASS | Todo model matches exactly |
| VI. Complete CRUD | ✅ PASS | All operations in service layer |
| VII. Clean CLI | ✅ PASS | Dedicated CLI layer with rich output |

**Final Gate Result**: ✅ READY FOR TASK GENERATION
