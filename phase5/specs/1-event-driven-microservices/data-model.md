# Data Model: Phase 5 Event-Driven Microservices

**Feature**: 1-event-driven-microservices
**Date**: 2026-01-30
**Status**: Complete

## Overview

This document defines entity schemas, relationships, and validation rules for Phase 5.

---

## Entity Definitions

### 1. Task (Enhanced)

**Storage**: PostgreSQL (Chat API database)
**Owner**: Chat API service

```
┌─────────────────────────────────────────────────────────────┐
│                         Task                                │
├─────────────────────────────────────────────────────────────┤
│ id              : UUID          [PK]                        │
│ title           : VARCHAR(255)  [NOT NULL]                  │
│ description     : TEXT          [NULLABLE]                  │
│ completed       : BOOLEAN       [NOT NULL, DEFAULT false]   │
│ created_at      : TIMESTAMPTZ   [NOT NULL, DEFAULT now()]   │
│ updated_at      : TIMESTAMPTZ   [NOT NULL, DEFAULT now()]   │
│ user_id         : UUID          [FK -> users.id, NOT NULL]  │
│ ─────────────── NEW FIELDS ──────────────────────────────── │
│ due_date        : TIMESTAMPTZ   [NULLABLE]                  │
│ priority        : VARCHAR(10)   [NOT NULL, DEFAULT 'NONE']  │
│ tags            : TEXT[]        [NOT NULL, DEFAULT '{}']    │
│ recurrence_rule : VARCHAR(255)  [NULLABLE]                  │
└─────────────────────────────────────────────────────────────┘

Constraints:
  - priority IN ('HIGH', 'MEDIUM', 'LOW', 'NONE')
  - recurrence_rule follows RFC 5545 RRULE format when present

Indexes:
  - idx_task_user_id ON (user_id)
  - idx_task_due_date ON (due_date) WHERE due_date IS NOT NULL
  - idx_task_priority ON (priority) WHERE priority != 'NONE'
  - idx_task_tags ON (tags) USING GIN
  - idx_task_title_desc ON (title, description) USING GIN (to_tsvector)
```

### 2. Reminder

**Storage**: Dapr State Store (Redis)
**Owner**: NotificationService

```
┌─────────────────────────────────────────────────────────────┐
│                       Reminder                              │
├─────────────────────────────────────────────────────────────┤
│ id              : UUID          [PK]                        │
│ task_id         : UUID          [NOT NULL]                  │
│ user_id         : UUID          [NOT NULL]                  │
│ trigger_time    : ISO8601       [NOT NULL]                  │
│ reminder_offset : VARCHAR(20)   [NOT NULL]                  │
│ status          : VARCHAR(20)   [NOT NULL, DEFAULT PENDING] │
│ created_at      : ISO8601       [NOT NULL]                  │
│ updated_at      : ISO8601       [NOT NULL]                  │
└─────────────────────────────────────────────────────────────┘

Constraints:
  - status IN ('PENDING', 'SENT', 'CANCELLED')
  - reminder_offset is ISO 8601 duration (e.g., 'PT1H', 'P1D')

State Key Pattern:
  - Primary: reminder:{id}
  - Index by task: reminder:task:{task_id}
  - Index by trigger: reminder:trigger:{YYYYMMDD}:{id}
```

### 3. AuditEntry

**Storage**: PostgreSQL (Audit Service database)
**Owner**: AuditService

```
┌─────────────────────────────────────────────────────────────┐
│                      AuditEntry                             │
├─────────────────────────────────────────────────────────────┤
│ id              : UUID          [PK]                        │
│ task_id         : UUID          [NOT NULL]                  │
│ user_id         : UUID          [NOT NULL]                  │
│ action          : VARCHAR(20)   [NOT NULL]                  │
│ timestamp       : TIMESTAMPTZ   [NOT NULL]                  │
│ before_state    : JSONB         [NULLABLE]                  │
│ after_state     : JSONB         [NOT NULL]                  │
│ metadata        : JSONB         [NOT NULL, DEFAULT '{}']    │
└─────────────────────────────────────────────────────────────┘

Constraints:
  - action IN ('CREATED', 'UPDATED', 'COMPLETED', 'DELETED')
  - before_state is NULL only when action = 'CREATED'

Indexes:
  - idx_audit_task_id ON (task_id)
  - idx_audit_user_id ON (user_id)
  - idx_audit_timestamp ON (timestamp)
  - idx_audit_action ON (action)

Metadata Fields:
  - correlation_id: UUID (traces event origin)
  - source: VARCHAR (e.g., 'chat-api', 'recurring-task-service')
  - actor: VARCHAR (user or system identifier)
```

### 4. Tag

**Storage**: Derived from Task.tags array (no separate table)
**Owner**: Chat API service

```
Tags are stored as an array on Task. Autocomplete queries aggregate
unique tags across user's tasks:

SELECT DISTINCT unnest(tags) AS tag
FROM tasks
WHERE user_id = $1
ORDER BY tag;
```

### 5. RecurrenceRule

**Storage**: Embedded in Task.recurrence_rule field
**Owner**: Chat API service (parsed by RecurringTaskService)

```
Format: RFC 5545 RRULE string

Examples:
  - Daily:              "FREQ=DAILY"
  - Every Monday:       "FREQ=WEEKLY;BYDAY=MO"
  - Monthly on 15th:    "FREQ=MONTHLY;BYMONTHDAY=15"
  - Last day of month:  "FREQ=MONTHLY;BYMONTHDAY=-1"
  - Every 2 weeks:      "FREQ=WEEKLY;INTERVAL=2"
  - Until date:         "FREQ=DAILY;UNTIL=20261231T235959Z"
  - N occurrences:      "FREQ=WEEKLY;COUNT=10"
```

---

## Event Schemas

### TaskEvent (CloudEvents)

```json
{
  "specversion": "1.0",
  "type": "com.todo.task.{action}",
  "source": "/services/chat-api",
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "time": "2026-01-30T12:00:00Z",
  "datacontenttype": "application/json",
  "data": {
    "taskId": "550e8400-e29b-41d4-a716-446655440001",
    "userId": "550e8400-e29b-41d4-a716-446655440002",
    "action": "CREATED | UPDATED | COMPLETED | DELETED",
    "task": {
      "id": "550e8400-e29b-41d4-a716-446655440001",
      "title": "Task title",
      "description": "Task description",
      "completed": false,
      "createdAt": "2026-01-30T10:00:00Z",
      "updatedAt": "2026-01-30T12:00:00Z",
      "userId": "550e8400-e29b-41d4-a716-446655440002",
      "dueDate": "2026-02-01T09:00:00Z",
      "priority": "HIGH",
      "tags": ["work", "urgent"],
      "recurrenceRule": "FREQ=WEEKLY;BYDAY=MO"
    },
    "changes": {
      "title": { "old": "Old title", "new": "New title" },
      "priority": { "old": "NONE", "new": "HIGH" }
    },
    "correlationId": "550e8400-e29b-41d4-a716-446655440003"
  }
}
```

**Event Types**:
- `com.todo.task.created` - New task created
- `com.todo.task.updated` - Task fields modified (includes `changes` diff)
- `com.todo.task.completed` - Task marked complete (`completed: true`)
- `com.todo.task.deleted` - Task soft/hard deleted

---

## State Transitions

### Task Lifecycle

```
┌─────────┐    create    ┌─────────┐    complete    ┌───────────┐
│ (none)  │ ──────────► │ PENDING │ ─────────────► │ COMPLETED │
└─────────┘              └─────────┘                └───────────┘
                              │                          │
                              │ update                   │ uncomplete
                              ▼                          │
                         ┌─────────┐                     │
                         │ PENDING │ ◄───────────────────┘
                         └─────────┘
                              │
                              │ delete
                              ▼
                         ┌─────────┐
                         │ DELETED │
                         └─────────┘
```

### Reminder Lifecycle

```
┌─────────┐    schedule    ┌─────────┐    trigger    ┌──────┐
│ (none)  │ ─────────────► │ PENDING │ ────────────► │ SENT │
└─────────┘                └─────────┘               └──────┘
                                │
                                │ task completed/deleted
                                ▼
                          ┌───────────┐
                          │ CANCELLED │
                          └───────────┘
```

### Recurring Task Flow

```
┌──────────────────┐
│ Task with RRULE  │
│ marked complete  │
└────────┬─────────┘
         │
         ▼
┌────────────────────────────┐
│ TaskCompleted event        │
│ published to task-events   │
└────────────┬───────────────┘
             │
             ▼
┌────────────────────────────┐
│ RecurringTaskService       │
│ consumes event             │
└────────────┬───────────────┘
             │
             ▼
┌────────────────────────────┐
│ Parse RRULE, calculate     │
│ next occurrence date       │
└────────────┬───────────────┘
             │
             ▼
┌────────────────────────────┐
│ Create new Task via        │
│ Dapr Service Invocation    │
│ to Chat API                │
└────────────┬───────────────┘
             │
             ▼
┌────────────────────────────┐
│ Chat API publishes         │
│ TaskCreated event          │
└────────────────────────────┘
```

---

## Relationships

```
┌────────────┐          ┌─────────────┐
│    User    │ 1 ─── * │    Task     │
└────────────┘          └──────┬──────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
        ▼                      ▼                      ▼
┌───────────────┐      ┌───────────────┐      ┌───────────────┐
│   Reminder    │      │  AuditEntry   │      │     Tag       │
│ (1:1 per due  │      │ (many per     │      │ (many:many    │
│  date)        │      │  task)        │      │  via array)   │
└───────────────┘      └───────────────┘      └───────────────┘
```

---

## Validation Rules

### Task
| Field | Validation |
|-------|------------|
| title | Required, 1-255 chars, trimmed |
| description | Optional, max 10000 chars |
| due_date | Optional, must be valid ISO 8601, future or today |
| priority | Must be one of: HIGH, MEDIUM, LOW, NONE |
| tags | Array of strings, each 1-50 chars, max 20 tags |
| recurrence_rule | Must be valid RFC 5545 RRULE if present |

### Reminder
| Field | Validation |
|-------|------------|
| task_id | Must reference existing task |
| trigger_time | Must be valid ISO 8601 |
| reminder_offset | Must be valid ISO 8601 duration |

### AuditEntry
| Field | Validation |
|-------|------------|
| task_id | UUID format |
| action | Must be one of: CREATED, UPDATED, COMPLETED, DELETED |
| before_state | Required unless action is CREATED |
| after_state | Required, must be valid task JSON |

---

## Database Migrations

### Migration 001: Add Task Enhancement Fields

```sql
-- Up
ALTER TABLE tasks ADD COLUMN due_date TIMESTAMPTZ;
ALTER TABLE tasks ADD COLUMN priority VARCHAR(10) NOT NULL DEFAULT 'NONE';
ALTER TABLE tasks ADD COLUMN tags TEXT[] NOT NULL DEFAULT '{}';
ALTER TABLE tasks ADD COLUMN recurrence_rule VARCHAR(255);

ALTER TABLE tasks ADD CONSTRAINT chk_priority
  CHECK (priority IN ('HIGH', 'MEDIUM', 'LOW', 'NONE'));

CREATE INDEX idx_task_due_date ON tasks (due_date) WHERE due_date IS NOT NULL;
CREATE INDEX idx_task_priority ON tasks (priority) WHERE priority != 'NONE';
CREATE INDEX idx_task_tags ON tasks USING GIN (tags);

-- Down
DROP INDEX IF EXISTS idx_task_tags;
DROP INDEX IF EXISTS idx_task_priority;
DROP INDEX IF EXISTS idx_task_due_date;
ALTER TABLE tasks DROP CONSTRAINT IF EXISTS chk_priority;
ALTER TABLE tasks DROP COLUMN IF EXISTS recurrence_rule;
ALTER TABLE tasks DROP COLUMN IF EXISTS tags;
ALTER TABLE tasks DROP COLUMN IF EXISTS priority;
ALTER TABLE tasks DROP COLUMN IF EXISTS due_date;
```

### Migration 002: Create Audit Entries Table

```sql
-- Up
CREATE TABLE audit_entries (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  task_id UUID NOT NULL,
  user_id UUID NOT NULL,
  action VARCHAR(20) NOT NULL,
  timestamp TIMESTAMPTZ NOT NULL DEFAULT now(),
  before_state JSONB,
  after_state JSONB NOT NULL,
  metadata JSONB NOT NULL DEFAULT '{}',
  CONSTRAINT chk_action CHECK (action IN ('CREATED', 'UPDATED', 'COMPLETED', 'DELETED'))
);

CREATE INDEX idx_audit_task_id ON audit_entries (task_id);
CREATE INDEX idx_audit_user_id ON audit_entries (user_id);
CREATE INDEX idx_audit_timestamp ON audit_entries (timestamp);
CREATE INDEX idx_audit_action ON audit_entries (action);

-- Down
DROP TABLE IF EXISTS audit_entries;
```

---

## References

- [RFC 5545 - iCalendar](https://datatracker.ietf.org/doc/html/rfc5545)
- [CloudEvents Specification](https://github.com/cloudevents/spec)
- [Dapr State Management](https://docs.dapr.io/developing-applications/building-blocks/state-management/)
