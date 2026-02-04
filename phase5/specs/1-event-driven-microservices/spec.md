# Feature Specification: Phase 5 Event-Driven Microservices

**Feature Branch**: `1-event-driven-microservices`
**Created**: 2026-01-30
**Status**: Draft
**Input**: User description: "Phase 5 advanced functionality for the Todo Chatbot with recurring tasks, due dates, reminders, priorities, tags, search/filter/sort, and event-driven architecture using Kafka topics with Dapr."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create and Manage Recurring Tasks (Priority: P1)

As a user, I want to create tasks that automatically repeat on a schedule (daily, weekly, monthly, or custom) so that I don't have to manually recreate routine tasks.

**Why this priority**: Recurring tasks are a core differentiator for Phase 5 and directly address user productivity. Without this, users must manually recreate repetitive tasks, which is the primary pain point this phase solves.

**Independent Test**: Can be fully tested by creating a recurring task, marking it complete, and verifying the next occurrence is automatically created. Delivers immediate value for routine task management.

**Acceptance Scenarios**:

1. **Given** a user is creating a new task, **When** they set a recurrence pattern (e.g., "every Monday"), **Then** the task is saved with the recurrence rule and displays the next occurrence date.
2. **Given** a recurring task exists, **When** the user marks it complete, **Then** the system automatically creates the next occurrence based on the recurrence rule within 5 seconds.
3. **Given** a recurring task exists, **When** the user edits the recurrence pattern, **Then** future occurrences reflect the new pattern (existing completed occurrences remain unchanged).
4. **Given** a recurring task exists, **When** the user deletes the recurrence rule, **Then** no further occurrences are created but the current task remains.

---

### User Story 2 - Due Dates and Reminder Notifications (Priority: P1)

As a user, I want to set due dates on tasks and receive reminders before they're due so that I never miss important deadlines.

**Why this priority**: Due dates and reminders are essential for task management and work in conjunction with recurring tasks. This is a foundational feature that all subsequent task organization builds upon.

**Independent Test**: Can be fully tested by creating a task with a due date, setting a reminder, and verifying the notification is delivered at the specified time. Delivers immediate value for deadline tracking.

**Acceptance Scenarios**:

1. **Given** a user is creating or editing a task, **When** they set a due date, **Then** the task displays the due date and is sortable/filterable by it.
2. **Given** a task has a due date, **When** the user sets a reminder (e.g., "1 hour before", "1 day before"), **Then** the system schedules a notification for that time.
3. **Given** a reminder is scheduled, **When** the reminder time arrives, **Then** the user receives a notification within 1 minute of the scheduled time.
4. **Given** a task with a reminder is completed before the reminder time, **When** the reminder time arrives, **Then** no notification is sent.
5. **Given** a task due date is changed, **When** an existing reminder is associated with it, **Then** the reminder is recalculated relative to the new due date.

---

### User Story 3 - Task Priorities and Organization (Priority: P2)

As a user, I want to assign priorities to tasks so that I can focus on what's most important first.

**Why this priority**: Priorities enhance task organization but are not blocking for core functionality. Users can still manage tasks effectively without priorities, but this significantly improves the experience.

**Independent Test**: Can be fully tested by creating tasks with different priorities and verifying they can be sorted and filtered by priority level. Delivers value for task triage and focus.

**Acceptance Scenarios**:

1. **Given** a user is creating or editing a task, **When** they assign a priority (High, Medium, Low, or None), **Then** the task displays the priority indicator.
2. **Given** multiple tasks exist with different priorities, **When** the user sorts by priority, **Then** tasks are ordered High → Medium → Low → None.
3. **Given** a task has a priority, **When** the user filters by that priority level, **Then** only tasks with the matching priority are displayed.

---

### User Story 4 - Tags and Categorization (Priority: P2)

As a user, I want to add tags to tasks so that I can categorize and group related tasks across projects or contexts.

**Why this priority**: Tags provide flexible organization complementing priorities. This is a power-user feature that enhances discoverability but doesn't block basic task management.

**Independent Test**: Can be fully tested by creating tasks with tags and verifying filtering by tag returns the correct tasks. Delivers value for cross-project organization.

**Acceptance Scenarios**:

1. **Given** a user is creating or editing a task, **When** they add one or more tags, **Then** the tags are saved and displayed on the task.
2. **Given** tasks exist with various tags, **When** the user filters by a specific tag, **Then** only tasks with that tag are displayed.
3. **Given** a user is adding tags, **When** they type a tag name, **Then** the system suggests existing tags for autocomplete.
4. **Given** a task has tags, **When** the user removes a tag, **Then** the tag is removed from that task but remains available for other tasks.

---

### User Story 5 - Search, Filter, and Sort Tasks (Priority: P2)

As a user, I want to search, filter, and sort my tasks so that I can quickly find and organize tasks based on various criteria.

**Why this priority**: Search and filtering significantly improve usability for users with many tasks, but basic task management works without it. This builds on priorities and tags.

**Independent Test**: Can be fully tested by creating multiple tasks and verifying search returns matching results, filters narrow the list correctly, and sorts reorder as expected.

**Acceptance Scenarios**:

1. **Given** tasks exist, **When** the user searches by keyword, **Then** tasks matching the keyword in title or description are displayed within 1 second.
2. **Given** tasks exist with due dates, **When** the user filters by date range, **Then** only tasks within that range are displayed.
3. **Given** tasks exist, **When** the user applies multiple filters (e.g., priority AND tag), **Then** only tasks matching all criteria are displayed.
4. **Given** filtered results exist, **When** the user applies a sort (by due date, priority, created date, or alphabetical), **Then** results are reordered accordingly.

---

### User Story 6 - Activity History and Audit Trail (Priority: P3)

As a user, I want to see a history of changes made to my tasks so that I can track what happened and when.

**Why this priority**: Audit trail is valuable for accountability and debugging but is not essential for daily task management. This is primarily consumed by power users and administrators.

**Independent Test**: Can be fully tested by creating, editing, and completing a task, then viewing its activity history showing all changes with timestamps.

**Acceptance Scenarios**:

1. **Given** any task change occurs (create, edit, complete, delete), **When** the change is processed, **Then** an audit entry is recorded with timestamp, action type, and before/after state.
2. **Given** a task has activity history, **When** the user views the task details, **Then** they can access a chronological list of all changes.
3. **Given** an administrator needs to review activity, **When** they query the audit log, **Then** they can filter by task ID, date range, action type, or user.

---

### User Story 7 - Real-Time Sync Across Devices (Priority: P3)

As a user, I want my task changes to sync in real-time across all my devices so that I always see the latest state.

**Why this priority**: Real-time sync enhances multi-device experience but users can still work effectively with eventual consistency. This leverages the event-driven architecture.

**Independent Test**: Can be fully tested by opening the app on two devices, making a change on one, and verifying the other device reflects the change within seconds.

**Acceptance Scenarios**:

1. **Given** a user has the app open on multiple devices, **When** a task is created/updated/deleted on one device, **Then** other devices reflect the change within 5 seconds.
2. **Given** a device was offline, **When** it reconnects, **Then** it receives all missed updates and displays the current state.

---

### Edge Cases

- What happens when a recurring task's next occurrence would fall on an invalid date (e.g., Feb 30)?
  - System adjusts to the last valid day of the month (e.g., Feb 28 or 29).
- What happens when a reminder is scheduled for a time that has already passed (e.g., user sets "1 day before" when due date is in 2 hours)?
  - Reminder is sent immediately or at the next reasonable interval (e.g., 1 hour before).
- What happens when a user creates a circular recurrence (e.g., task recurs on completion but is never completed)?
  - Only one pending occurrence exists at a time; new occurrence created only when current is completed.
- What happens when search returns thousands of results?
  - Results are paginated with reasonable page sizes (e.g., 50 items) and total count displayed.
- What happens when a task is edited while another device is viewing it?
  - Viewing device receives update event and refreshes display; no data loss.
- What happens when Kafka/messaging is temporarily unavailable?
  - Events are queued locally and processed when connectivity resumes; user operations are not blocked.

## Requirements *(mandatory)*

### Functional Requirements

**Task Enhancements**
- **FR-001**: System MUST allow users to set recurrence rules on tasks (daily, weekly, monthly, yearly, or custom patterns).
- **FR-002**: System MUST automatically create the next occurrence of a recurring task within 5 seconds of the previous occurrence being completed.
- **FR-003**: System MUST allow users to set due dates on tasks with date and optional time.
- **FR-004**: System MUST allow users to set reminders relative to due dates (e.g., 15 minutes, 1 hour, 1 day before).
- **FR-005**: System MUST deliver reminder notifications within 1 minute of the scheduled time.
- **FR-006**: System MUST allow users to assign priority levels (High, Medium, Low, None) to tasks.
- **FR-007**: System MUST allow users to add, remove, and edit tags on tasks.
- **FR-008**: System MUST support searching tasks by keyword across title and description.
- **FR-009**: System MUST support filtering tasks by due date range, priority, tags, and completion status.
- **FR-010**: System MUST support sorting tasks by due date, priority, created date, and alphabetical order.

**Event-Driven Architecture**
- **FR-011**: System MUST publish events for all task state changes (created, updated, completed, deleted) to a message broker.
- **FR-012**: System MUST consume task events to trigger recurring task creation via a dedicated service.
- **FR-013**: System MUST consume task events to schedule and send reminders via a dedicated notification service.
- **FR-014**: System MUST consume task events to record audit entries via a dedicated audit service.
- **FR-015**: System MUST publish task update events to enable real-time synchronization across clients.
- **FR-016**: System MUST use Dapr Pub/Sub for all service-to-service event communication.
- **FR-017**: System MUST use Dapr State Store for service-specific state (conversation metadata, recurrence tracking).
- **FR-018**: System MUST use Dapr Cron Bindings for scheduled reminder triggers.
- **FR-019**: System MUST use Dapr Service Invocation for synchronous service-to-service calls.
- **FR-020**: System MUST use Dapr Secrets for all credential and configuration management.

**Deployment & Operations**
- **FR-021**: System MUST deploy to local Minikube with self-hosted Kafka without code changes.
- **FR-022**: System MUST deploy to cloud Kubernetes (AKS/GKE/OKE) with managed Kafka without code changes.
- **FR-023**: System MUST provide Helm charts for all services with environment-specific values files.
- **FR-024**: System MUST NOT modify existing CRUD API endpoints or frontend behavior.

### Key Entities

- **Task** (enhanced): Existing task entity extended with due_date, reminder_settings, recurrence_rule, priority, and tags attributes.
- **RecurrenceRule**: Defines the pattern for recurring tasks (frequency, interval, end conditions). Linked to a Task.
- **Reminder**: Scheduled notification with target time, delivery status, and associated task reference.
- **AuditEntry**: Immutable record of a task change with timestamp, action type, actor, and before/after snapshots.
- **Tag**: Named label that can be associated with multiple tasks. Supports user-defined categorization.
- **TaskEvent**: Immutable event payload containing task snapshot, action type, timestamp, and metadata for event-driven communication.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can create a recurring task and see the next occurrence auto-created within 5 seconds of completing the current one.
- **SC-002**: Users receive reminder notifications within 1 minute of the scheduled time with 99% reliability.
- **SC-003**: Users can search across 10,000+ tasks and receive results within 1 second.
- **SC-004**: Users can filter and sort task lists with results updating in under 500 milliseconds.
- **SC-005**: Task changes sync to other connected devices within 5 seconds.
- **SC-006**: All task changes are recorded in the audit log with complete before/after state.
- **SC-007**: System deploys to both Minikube and cloud Kubernetes using the same Helm charts with only values file differences.
- **SC-008**: Existing CRUD operations continue to function with zero breaking changes.
- **SC-009**: System handles 1,000 concurrent users with no degradation in response times.
- **SC-010**: Microservices operate independently—failure of one service (e.g., Notification) does not block core task operations.

## Scope Boundaries *(mandatory)*

### In Scope

- Recurring task creation and automatic next-occurrence generation
- Due dates and time-based reminders
- Priority levels (High, Medium, Low, None)
- User-defined tags with autocomplete
- Search, filter, and sort capabilities
- Event-driven architecture with three microservices (Recurring, Notification, Audit)
- Dapr integration (Pub/Sub, State, Bindings, Service Invocation, Secrets)
- Kafka as message broker (self-hosted and managed)
- Helm charts for all services
- Real-time sync via events

### Out of Scope

- UI redesign or major frontend changes
- Changes to existing CRUD API endpoints
- User authentication/authorization changes
- Mobile push notifications (in-app only for this phase)
- Natural language processing for recurrence (e.g., "every other Tuesday")
- Task sharing or collaboration features
- File attachments on tasks
- Subtasks or task hierarchies

## Assumptions

- Existing Phase 4 Kubernetes deployment is stable and can be extended without modification.
- Dapr sidecar injection is available and configured in the Kubernetes cluster.
- Kafka (self-hosted or managed) is available in target environments.
- Users have a single active session for real-time sync (multi-session sync is eventual consistency).
- Reminder notification delivery is in-app; external delivery (email, SMS) is future scope.
- Tag autocomplete suggestions are scoped to the current user's tags only.
- Priority levels are fixed (not user-customizable) for this phase.
- Recurrence patterns follow iCalendar RRULE standard for interoperability.

## Dependencies

- **Phase 4 Todo Chatbot**: Core CRUD API and Kubernetes deployment must be operational.
- **Dapr Runtime**: Version 1.10+ required for all building blocks.
- **Kafka**: Apache Kafka 3.x or compatible (Redpanda, Confluent) for Pub/Sub backend.
- **Kubernetes**: Minikube 1.30+ for local; AKS/GKE/OKE for cloud deployment.
- **Helm**: Version 3.x for chart deployment.

## Risks

- **Event ordering**: Out-of-order event delivery could cause inconsistent state. Mitigation: Include sequence numbers and idempotency keys in events.
- **Kafka availability**: Messaging downtime could delay recurring tasks and reminders. Mitigation: Local event queue with retry; graceful degradation.
- **Clock skew**: Reminder timing depends on synchronized clocks across services. Mitigation: Use UTC timestamps; tolerate ±1 minute variance.
