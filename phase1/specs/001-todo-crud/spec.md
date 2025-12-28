# Feature Specification: Phase 1 In-Memory Todo CRUD Application

**Feature Branch**: `001-todo-crud`
**Created**: 2025-12-27
**Status**: Draft
**Constitution Reference**: `.specify/memory/constitution.md` v1.0.0

## Overview

This specification defines a Python console application for managing todo items entirely in memory. The application provides a complete CRUD (Create, Read, Update, Delete) interface plus completion status toggling, all through an interactive command-line interface.

### Scope Boundaries

**In Scope**:
- Interactive console menu using questionary
- Formatted output using rich
- In-memory storage (data lost on exit)
- Single-user operation
- Basic todo entity: ID, title, completion status

**Out of Scope** (per Constitution v1.0.0):
- Data persistence (database, file storage)
- Multi-user support or authentication
- Web interface or API
- Extended fields (due dates, priorities, categories)
- Search or filtering

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Add New Todo (Priority: P1)

As a user, I want to add a new todo item so that I can track tasks I need to complete.

**Why this priority**: Creating todos is the foundational operation. Without the ability to add items, no other operations are meaningful. This is the entry point for all user value.

**Independent Test**: Can be fully tested by launching the app, selecting "Add Todo", entering a title, and verifying the todo appears in the list. Delivers immediate value as a basic task capture tool.

**Acceptance Scenarios**:

1. **Given** the application is running with an empty todo list, **When** the user selects "Add Todo" and enters "Buy groceries", **Then** a new todo with title "Buy groceries" is created with a unique ID and completion status of incomplete, and a success message is displayed.

2. **Given** the application is running with existing todos, **When** the user adds a new todo, **Then** the new todo receives a unique ID that does not conflict with existing IDs.

3. **Given** the user is prompted to enter a todo title, **When** the user enters only whitespace or an empty string, **Then** an error message is displayed and the user is prompted to enter a valid title.

---

### User Story 2 - View All Todos (Priority: P1)

As a user, I want to view all my todos in a formatted list so that I can see what tasks I need to complete.

**Why this priority**: Viewing todos is essential for the user to understand their current task state. Without visibility, users cannot make decisions about what to work on next.

**Independent Test**: Can be tested by adding several todos, selecting "View Todos", and verifying all items appear in a formatted table with ID, title, and completion status clearly visible.

**Acceptance Scenarios**:

1. **Given** todos exist in the system, **When** the user selects "View Todos", **Then** all todos are displayed in a formatted table showing ID, title, and completion status.

2. **Given** no todos exist in the system, **When** the user selects "View Todos", **Then** a friendly message indicates the list is empty (e.g., "No todos yet. Add one to get started!").

3. **Given** todos with mixed completion statuses exist, **When** the user views the list, **Then** completed todos are visually distinguished from incomplete todos (e.g., strikethrough, different color, or checkmark indicator).

---

### User Story 3 - Mark Todo Complete/Incomplete (Priority: P2)

As a user, I want to toggle a todo's completion status so that I can track my progress on tasks.

**Why this priority**: Toggling completion is core to task management value. However, it depends on having todos to toggle (P1 stories), making it a secondary priority.

**Independent Test**: Can be tested by adding a todo, toggling its status, viewing the list to confirm the change, and toggling again to verify the reverse works.

**Acceptance Scenarios**:

1. **Given** an incomplete todo exists, **When** the user selects "Toggle Complete" and chooses that todo, **Then** the todo's status changes to complete and a confirmation message is displayed.

2. **Given** a completed todo exists, **When** the user selects "Toggle Complete" and chooses that todo, **Then** the todo's status changes to incomplete and a confirmation message is displayed.

3. **Given** no todos exist, **When** the user selects "Toggle Complete", **Then** a message indicates there are no todos to toggle.

---

### User Story 4 - Update Todo Title (Priority: P3)

As a user, I want to update a todo's title so that I can correct mistakes or refine task descriptions.

**Why this priority**: Updates are important but less frequent than core add/view/complete operations. Users can work around missing update by deleting and re-adding.

**Independent Test**: Can be tested by adding a todo with a title, selecting "Update Todo", choosing the todo, entering a new title, and verifying the change in the list view.

**Acceptance Scenarios**:

1. **Given** a todo exists with title "Buy groceries", **When** the user selects "Update Todo", chooses that todo, and enters "Buy organic groceries", **Then** the todo's title is updated and a confirmation message is displayed.

2. **Given** the user is updating a todo's title, **When** the user enters only whitespace or an empty string, **Then** an error message is displayed and the original title is preserved.

3. **Given** no todos exist, **When** the user selects "Update Todo", **Then** a message indicates there are no todos to update.

---

### User Story 5 - Delete Todo (Priority: P3)

As a user, I want to delete a todo so that I can remove tasks that are no longer relevant.

**Why this priority**: Delete is a cleanup operation. While useful, users can work around it by simply ignoring completed items. The destructive nature also means it requires careful UX.

**Independent Test**: Can be tested by adding a todo, selecting "Delete Todo", confirming the deletion, and verifying the todo no longer appears in the list.

**Acceptance Scenarios**:

1. **Given** a todo exists, **When** the user selects "Delete Todo" and confirms the deletion, **Then** the todo is permanently removed and a confirmation message is displayed.

2. **Given** a todo exists, **When** the user selects "Delete Todo" but cancels the confirmation, **Then** the todo is preserved and the user returns to the main menu.

3. **Given** no todos exist, **When** the user selects "Delete Todo", **Then** a message indicates there are no todos to delete.

---

### User Story 6 - Exit Application (Priority: P1)

As a user, I want to exit the application gracefully so that I can end my session cleanly.

**Why this priority**: Exit is essential for application usability. Users must be able to close the app without errors.

**Independent Test**: Can be tested by selecting "Exit" from the menu and verifying the application terminates without errors.

**Acceptance Scenarios**:

1. **Given** the application is running, **When** the user selects "Exit", **Then** the application terminates gracefully with a goodbye message.

2. **Given** the application is running with unsaved todos, **When** the user selects "Exit", **Then** the application terminates (in-memory data is expected to be lost per constitution).

---

### Edge Cases

- **Empty title handling**: Whitespace-only or empty titles MUST be rejected with a clear error message
- **ID uniqueness**: Each todo MUST have a unique ID that never changes and is never reused
- **Empty list operations**: Update, delete, and toggle operations on an empty list MUST display a helpful message instead of crashing
- **Keyboard interrupt**: Ctrl+C during input MUST not crash the application; graceful handling is expected
- **Very long titles**: Titles exceeding display width MUST be handled gracefully (truncation or wrapping)
- **Special characters**: Titles containing special characters (quotes, newlines, unicode) MUST be preserved correctly

## Requirements *(mandatory)*

### Functional Requirements

#### Todo Entity

- **FR-001**: Each todo MUST have a unique, system-generated, immutable identifier
- **FR-002**: Each todo MUST have a title (non-empty string provided by user)
- **FR-003**: Each todo MUST have a completion status (boolean, default: incomplete)
- **FR-004**: Todo IDs MUST remain stable for the lifetime of the todo (never change)
- **FR-005**: Todo IDs MUST never be reused within a session

#### Add Todo

- **FR-010**: System MUST allow users to create new todos with a title
- **FR-011**: System MUST reject empty or whitespace-only titles with an error message
- **FR-012**: System MUST assign a unique ID to each new todo automatically
- **FR-013**: System MUST set new todos to incomplete status by default
- **FR-014**: System MUST confirm successful todo creation to the user

#### View Todos

- **FR-020**: System MUST display all todos in a formatted, readable table
- **FR-021**: Table MUST show each todo's ID, title, and completion status
- **FR-022**: Completed todos MUST be visually distinguished from incomplete todos
- **FR-023**: System MUST display a friendly message when no todos exist

#### Update Todo

- **FR-030**: System MUST allow users to select a todo and update its title
- **FR-031**: System MUST reject empty or whitespace-only titles with an error message
- **FR-032**: System MUST preserve the original title if update validation fails
- **FR-033**: System MUST confirm successful title update to the user
- **FR-034**: System MUST display a message when attempting to update with no todos

#### Delete Todo

- **FR-040**: System MUST allow users to select a todo for deletion
- **FR-041**: System MUST require confirmation before deleting a todo
- **FR-042**: System MUST permanently remove the todo upon confirmation
- **FR-043**: System MUST cancel deletion if user declines confirmation
- **FR-044**: System MUST confirm successful deletion to the user
- **FR-045**: System MUST display a message when attempting to delete with no todos

#### Toggle Completion

- **FR-050**: System MUST allow users to toggle a todo's completion status
- **FR-051**: Toggling an incomplete todo MUST mark it as complete
- **FR-052**: Toggling a complete todo MUST mark it as incomplete
- **FR-053**: System MUST confirm the status change to the user
- **FR-054**: System MUST display a message when attempting to toggle with no todos

#### Application Lifecycle

- **FR-060**: System MUST provide an interactive menu for all operations
- **FR-061**: System MUST return to the main menu after each operation completes
- **FR-062**: System MUST provide a clean exit option
- **FR-063**: System MUST display a goodbye message on exit
- **FR-064**: System MUST handle keyboard interrupts gracefully without crashing

#### Data Storage

- **FR-070**: All todo data MUST be stored in memory only
- **FR-071**: System MUST NOT persist data between sessions
- **FR-072**: System MUST NOT read or write to any files for todo storage

### Key Entities

- **Todo**: The primary entity representing a task to be completed
  - Attributes: id (unique identifier), title (string), completed (boolean)
  - Created via "Add Todo" operation
  - Modified via "Update Todo" and "Toggle Complete" operations
  - Removed via "Delete Todo" operation

- **TodoList**: The in-memory collection of all todos
  - Contains zero or more Todo items
  - Provides operations: add, get_all, get_by_id, update, delete
  - Exists only for the duration of the application session

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can add a new todo in under 10 seconds from menu selection to confirmation
- **SC-002**: Users can view their complete todo list in under 2 seconds
- **SC-003**: Users can toggle a todo's completion status in under 5 seconds from menu selection
- **SC-004**: Users can update a todo's title in under 15 seconds from menu selection to confirmation
- **SC-005**: Users can delete a todo in under 10 seconds from menu selection to confirmation
- **SC-006**: 100% of invalid inputs (empty titles, operations on empty lists) result in helpful error messages instead of crashes
- **SC-007**: Application exits cleanly with no errors when user selects "Exit"
- **SC-008**: All operations return to the main menu, allowing continuous workflow

### Quality Outcomes

- **SC-010**: First-time users can complete all CRUD operations without external documentation
- **SC-011**: Todo list display clearly distinguishes completed from incomplete items
- **SC-012**: Error messages clearly explain what went wrong and how to proceed
- **SC-013**: Confirmation prompts prevent accidental data loss (delete operation)

## Assumptions

The following assumptions were made based on the constitution and standard practices:

1. **ID Format**: Integer IDs starting from 1, incrementing by 1 for each new todo (simple, predictable)
2. **Title Length**: No maximum length enforced in Phase 1; display handles long titles gracefully
3. **Session Scope**: Single session = one application run; restart means fresh empty state
4. **Menu Style**: questionary select-style menu for main operations, text input for titles
5. **Confirmation Style**: Yes/No confirmation for delete only (destructive operation)
6. **Visual Distinction**: Completed todos shown with checkmark or strikethrough styling via rich
