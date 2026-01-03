# Feature Specification: Phase 2 Core Features

**Feature Branch**: `main`
**Created**: 2026-01-01
**Status**: Draft
**Input**: Create a clear functional specification for Phase 2 of the Todo App including User auth, Task CRUD, Task ownership, and layer responsibilities.

## User Scenarios & Testing

### User Story 1 - Secure Task Management (Priority: P1)
As a user, I want to create an account and manage my tasks securely so that my data is private and accessible only to me.

**Why this priority**: Core functionality that defines the multi-user nature of the application.
**Independent Test**: Register a user, create a task, log out, register a second user, and verify the first user's task is not visible.
**Acceptance Scenarios**:
1. **Given** a new visitor, **When** they sign up with valid credentials, **Then** an account is created and they are logged in.
2. **Given** a logged-in user, **When** they create a task, **Then** the task appears in their list and is persisted in the database with their ID.
3. **Given** a direct URL or API call to another user's task, **When** a user attempts to access it, **Then** the system returns an "unauthorized" error.

### User Story 2 - Task Lifecycle (Priority: P2)
As a user, I want to be able to read, update, and delete my tasks so that I can manage my todo list effectively.

**Why this priority**: Essential CRUD operations for utility.
**Independent Test**: Create a task, update its status, and delete it, verifying changes reflect immediately.
**Acceptance Scenarios**:
1. **Given** an existing task, **When** the user changes its status from "pending" to "completed", **Then** the update is persisted and reflected in the UI.
2. **Given** an existing task, **When** the user deletes it, **Then** it is permanently removed and disappears from the UI.

## Requirements

### Functional Requirements
- **FR-001**: System MUST support secure user registration (signup).
- **FR-002**: System MUST support secure user authentication (login/logout).
- **FR-003**: System MUST permit users to create new tasks with a title.
- **FR-004**: System MUST display a list of tasks belonging ONLY to the authenticated user.
- **FR-005**: System MUST allow users to update the title or status of their own tasks.
- **FR-006**: System MUST allow users to delete their own tasks.
- **FR-007**: System MUST automatically record creation and update timestamps for every task.

### Key Entities
- **User**: Represents a registered individual. Attributes: unique ID, authentication credentials.
- **Task**: Represents a todo item. Attributes: unique ID, title, status (e.g., pending/completed), creation timestamp, last updated timestamp, and an owner ID (reference to User).

## Layer Responsibilities

### Frontend (Next.js)
- Provide user interfaces for signup, login, and task management.
- Manage client-side authentication state and protect private routes.
- Communicate with the Backend API for all data operations.
- Handle and display success/error feedback (e.g., validation errors, auth failures).
- Maintain responsive UI state during asynchronous operations.

### Backend (FastAPI)
- Expose RESTful API endpoints for authentication and task CRUD.
- Enforce strict authentication and authorization checks (verify user identity and data ownership per request).
- Validate all incoming data before processing or persistence.
- Interface with the database using an ORM or database driver.
- Return appropriate HTTP status codes and structured error messages.

### Database (Neon PostgreSQL)
- Persist User and Task records reliably.
- Enforce relational integrity (e.g., Task ownership via Foreign Keys).
- Support efficient querying for per-user task lists.
- Maintain data consistency through ACID transactions.

## Success Criteria

### Measurable Outcomes
- **SC-001**: 100% of tasks in the database are correctly associated with a valid User ID.
- **SC-002**: Unauthorized attempts to access another user's task via the API are blocked with a 403 Forbidden or 404 Not Found error.
- **SC-003**: Users can transition from the index page to a successful login and see their tasks in under 2 seconds.
- **SC-004**: System correctly handles concurrent task updates from multiple authenticated users without data leakage.

## Edge Cases
- **Duplicate User**: Handing registration attempts with an existing email/username.
- **Session Expiry**: Behavior when a user's session token expires during an active session (e.g., prompt for re-login).
- **Empty Task Title**: Preventing or handling creation of tasks with no content.
- **Network Failure**: Frontend behavior when the backend API is unreachable.
