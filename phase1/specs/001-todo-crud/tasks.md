# Tasks: Phase 1 In-Memory Todo CRUD Application

**Input**: Design documents from `/specs/001-todo-crud/`
**Prerequisites**: plan.md (required), spec.md (required), data-model.md, contracts/
**Branch**: `001-todo-crud`
**Date**: 2025-12-27

**Tests**: Tests are OPTIONAL for Phase 1. Unit tests included in Polish phase for validation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below follow the plan.md structure

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Project initialization and basic structure

- [x] T001 Initialize uv project with pyproject.toml at repository root
- [x] T002 [P] Add runtime dependencies: questionary>=2.0.0, rich>=13.0.0 via `uv add`
- [x] T003 [P] Add dev dependencies: pytest>=8.0.0, pytest-cov>=4.0.0 via `uv add --dev`
- [x] T004 Create src/ directory structure with __init__.py files:
  - src/__init__.py
  - src/models/__init__.py
  - src/services/__init__.py
  - src/storage/__init__.py
  - src/cli/__init__.py
- [x] T005 [P] Create tests/ directory structure with __init__.py files:
  - tests/__init__.py
  - tests/unit/__init__.py
  - tests/integration/__init__.py

**Checkpoint**: Project structure ready, dependencies installed

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T006 Create Todo dataclass entity in src/models/todo.py with:
  - id: int
  - title: str
  - completed: bool = False
  - toggle() method to flip completed status
- [x] T007 Create ValidationError exception class in src/models/todo.py
- [x] T008 Create TodoNotFoundError exception class in src/models/todo.py
- [x] T009 Create MemoryStore class in src/storage/memory_store.py with:
  - _todos: dict[int, Todo]
  - _next_id: int = 1
  - add(title: str) -> Todo
  - get_all() -> list[Todo]
  - get_by_id(todo_id: int) -> Todo | None
  - update(todo_id: int, title: str) -> Todo | None
  - delete(todo_id: int) -> bool
  - count() -> int
  - is_empty() -> bool
- [x] T010 Create TodoService class in src/services/todo_service.py with:
  - _store: MemoryStore (injected or created)
  - validate_title(title: str) -> str (raises ValidationError if empty)
  - add_todo(title: str) -> Todo
  - get_all_todos() -> list[Todo]
  - get_todo_by_id(todo_id: int) -> Todo | None
  - update_todo(todo_id: int, new_title: str) -> Todo
  - delete_todo(todo_id: int) -> bool
  - toggle_complete(todo_id: int) -> Todo
  - has_todos() -> bool
- [x] T011 Create display module in src/cli/display.py with:
  - Console instance from rich
  - show_success(message: str)
  - show_error(message: str)
  - show_warning(message: str)
  - show_todo_table(todos: list[Todo])
  - show_empty_list_message()
  - show_goodbye()

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 & 2 - Add Todo & View Todos (Priority: P1) MVP

**Goal**: Users can add todos and view them in a formatted list

**Independent Test**: Launch app, add a todo, view the list - should see the added todo

**Why Combined**: Add and View are tightly coupled for MVP - you need View to verify Add works

### Implementation for User Stories 1 & 2

- [x] T012 [US1] Create handle_add_todo function in src/cli/handlers.py:
  - Prompt for title using questionary.text()
  - Call service.add_todo(title)
  - Display success message with todo ID
  - Handle ValidationError with error message
  - Handle KeyboardInterrupt gracefully
- [x] T013 [US2] Create handle_view_todos function in src/cli/handlers.py:
  - Call service.get_all_todos()
  - If empty: show empty list message
  - If has todos: display formatted table using display module
- [x] T014 [US1][US2] Create main menu in src/cli/menu.py with:
  - show_menu() function using questionary.select()
  - Menu choices: Add Todo, View Todos, Exit (minimal MVP)
  - Return selected action key
- [x] T015 [US1][US2] Create application entry point in src/main.py:
  - Initialize TodoService
  - Main loop calling show_menu() and routing to handlers
  - Handle Exit option with goodbye message
  - Wrap in try/except KeyboardInterrupt

**Checkpoint**: MVP complete - users can add and view todos

---

## Phase 4: User Story 6 - Exit Application (Priority: P1)

**Goal**: Users can exit the application gracefully

**Independent Test**: Select Exit from menu, verify goodbye message and clean termination

### Implementation for User Story 6

- [x] T016 [US6] Add Exit handling in src/main.py:
  - Detect "exit" action from menu
  - Call display.show_goodbye()
  - Break from main loop
- [x] T017 [US6] Update src/cli/display.py show_goodbye():
  - Display "Goodbye! Your todos have not been saved."
  - Use yellow color for warning about unsaved data

**Checkpoint**: All P1 stories complete (Add, View, Exit)

---

## Phase 5: User Story 3 - Toggle Complete/Incomplete (Priority: P2)

**Goal**: Users can mark todos as complete or incomplete

**Independent Test**: Add a todo, toggle it complete, view list shows checkmark, toggle again shows pending

### Implementation for User Story 3

- [x] T018 [US3] Add todo selection helper in src/cli/handlers.py:
  - select_todo(todos: list[Todo], prompt: str) -> Todo | None
  - Format choices as "[id] status title"
  - Use questionary.select()
  - Return selected Todo or None if cancelled
- [x] T019 [US3] Create handle_toggle_complete function in src/cli/handlers.py:
  - Check if todos exist, show message if empty
  - Call select_todo() to choose a todo
  - Call service.toggle_complete(todo_id)
  - Display confirmation with new status
- [x] T020 [US3] Update main menu in src/cli/menu.py:
  - Add "Toggle Complete" option to menu choices
  - Map to "toggle" action key
- [x] T021 [US3] Update main loop in src/main.py:
  - Add routing for "toggle" action to handle_toggle_complete

**Checkpoint**: Users can track completion status

---

## Phase 6: User Story 4 - Update Todo Title (Priority: P3)

**Goal**: Users can modify existing todo titles

**Independent Test**: Add todo, update its title, view shows new title

### Implementation for User Story 4

- [x] T022 [US4] Create handle_update_todo function in src/cli/handlers.py:
  - Check if todos exist, show message if empty
  - Call select_todo() to choose a todo
  - Prompt for new title using questionary.text()
  - Call service.update_todo(todo_id, new_title)
  - Display confirmation with old → new title
  - Handle ValidationError with error message
- [x] T023 [US4] Update main menu in src/cli/menu.py:
  - Add "Update Todo" option to menu choices
  - Map to "update" action key
- [x] T024 [US4] Update main loop in src/main.py:
  - Add routing for "update" action to handle_update_todo

**Checkpoint**: Users can correct todo titles

---

## Phase 7: User Story 5 - Delete Todo (Priority: P3)

**Goal**: Users can remove todos permanently with confirmation

**Independent Test**: Add todo, delete it with confirmation, verify removed from list

### Implementation for User Story 5

- [x] T025 [US5] Create handle_delete_todo function in src/cli/handlers.py:
  - Check if todos exist, show message if empty
  - Call select_todo() to choose a todo
  - Prompt for confirmation using questionary.confirm()
  - If confirmed: call service.delete_todo(todo_id), show success
  - If cancelled: show "Deletion cancelled"
- [x] T026 [US5] Update main menu in src/cli/menu.py:
  - Add "Delete Todo" option to menu choices
  - Map to "delete" action key
- [x] T027 [US5] Update main loop in src/main.py:
  - Add routing for "delete" action to handle_delete_todo

**Checkpoint**: All CRUD operations complete

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T028 [P] Add keyboard interrupt handling in src/main.py:
  - Wrap entire main() in try/except KeyboardInterrupt
  - Display "Goodbye!" message on interrupt
  - Exit cleanly without stack trace
- [x] T029 [P] Verify all edge cases in src/cli/handlers.py:
  - Empty title validation works for add and update
  - Empty list messages work for toggle, update, delete
  - Cancel/escape handling works for all operations
- [x] T030 [P] Create unit tests in tests/unit/test_todo.py:
  - test_todo_creation
  - test_todo_toggle
  - test_todo_default_incomplete
- [x] T031 [P] Create unit tests in tests/unit/test_memory_store.py:
  - test_add_todo
  - test_get_all_todos
  - test_get_by_id
  - test_update_todo
  - test_delete_todo
  - test_id_never_reused
- [x] T032 [P] Create unit tests in tests/unit/test_todo_service.py:
  - test_add_todo_success
  - test_add_todo_empty_title
  - test_toggle_complete
  - test_update_todo
  - test_delete_todo
- [x] T033 Run all tests and verify 100% pass rate
- [x] T034 Run quickstart.md verification checklist manually

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1: Setup
    │
    ▼
Phase 2: Foundational (BLOCKS all user stories)
    │
    ├──────────────────────────────────────┐
    ▼                                      ▼
Phase 3: US1+US2 (Add/View)           [Can run in parallel
    │                                  if team capacity allows]
    ▼
Phase 4: US6 (Exit)
    │
    ▼
Phase 5: US3 (Toggle) ◄─── Depends on Add/View being complete
    │
    ▼
Phase 6: US4 (Update)
    │
    ▼
Phase 7: US5 (Delete)
    │
    ▼
Phase 8: Polish
```

### Task Dependencies Within Phases

- **Phase 1**: T001 first, then T002-T005 in parallel
- **Phase 2**: T006-T008 → T009 → T010 → T011
- **Phase 3**: T012-T013 can parallel → T014 → T015
- **Phase 4**: T016 → T017
- **Phase 5**: T018 → T019 → T020 → T021
- **Phase 6**: T022 → T023 → T024
- **Phase 7**: T025 → T026 → T027
- **Phase 8**: T028-T032 all parallel, T033-T034 sequential at end

### Parallel Opportunities

```bash
# Phase 1 parallel tasks (after T001):
T002, T003, T004, T005

# Phase 2 parallel tasks (after T010):
T007, T008 (exceptions can be created in parallel)

# Phase 3 parallel tasks:
T012, T013 (handlers can be created in parallel)

# Phase 8 parallel tasks:
T028, T029, T030, T031, T032 (all independent)
```

---

## Implementation Strategy

### MVP First (Phases 1-4 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Stories 1+2 (Add + View)
4. Complete Phase 4: User Story 6 (Exit)
5. **STOP and VALIDATE**: Test Add/View/Exit independently
6. Deploy/demo if ready - this is a functional MVP

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. Add User Stories 1+2+6 → MVP ready (Add/View/Exit)
3. Add User Story 3 → Toggle complete functionality
4. Add User Story 4 → Update functionality
5. Add User Story 5 → Delete functionality
6. Polish → Tests, edge cases, cleanup

### Estimated Task Counts

| Phase | Tasks | Parallel Opportunities |
|-------|-------|------------------------|
| Phase 1: Setup | 5 | 4 |
| Phase 2: Foundational | 6 | 2 |
| Phase 3: US1+US2 | 4 | 2 |
| Phase 4: US6 | 2 | 0 |
| Phase 5: US3 | 4 | 0 |
| Phase 6: US4 | 3 | 0 |
| Phase 7: US5 | 3 | 0 |
| Phase 8: Polish | 7 | 5 |
| **Total** | **34** | **13** |

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

## Constitution Compliance

| Principle | Tasks Supporting |
|-----------|------------------|
| I. Spec-Driven | All tasks derived from spec.md requirements |
| II. Reusable Intelligence | Layer separation enables future reuse |
| III. In-Memory Simplicity | T009 MemoryStore, no persistence tasks |
| IV. Minimal Dependencies | T002-T003 only questionary+rich+pytest |
| V. Todo Entity Contract | T006 matches exact contract |
| VI. Complete CRUD | T012-T027 cover all operations |
| VII. Clean CLI | T011-T027 use questionary+rich properly |
