# Tasks: Phase 5 Event-Driven Microservices

**Input**: Design documents from `/specs/1-event-driven-microservices/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/
**Date**: 2026-01-30

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1-US7)
- All file paths are relative to repository root

## Path Conventions (Microservices Architecture)

```
services/
├── chat-api/                    # Existing (add events/ module)
├── recurring-task-service/      # NEW
├── notification-service/        # NEW
└── audit-service/               # NEW

helm/
├── todo-chatbot/                # Umbrella chart
├── strimzi-kafka/               # Local Kafka
└── dapr-components/             # Dapr configs

.github/workflows/               # CI/CD pipelines
```

---

## Phase 1: Setup (Infrastructure Foundation)

**Purpose**: Install Kubernetes infrastructure (Dapr, Kafka, Redis) required by all services

- [ ] T001 Create Strimzi Kafka operator Helm chart in helm/strimzi-kafka/Chart.yaml
- [ ] T002 [P] Create Kafka cluster manifest in helm/strimzi-kafka/templates/kafka-cluster.yaml
- [ ] T003 [P] Create Kafka topics manifest (task-events, task-reminders, task-updates) in helm/strimzi-kafka/templates/kafka-topics.yaml
- [ ] T004 Create Dapr components Helm chart in helm/dapr-components/Chart.yaml
- [ ] T005 [P] Create Dapr Pub/Sub component (Kafka) in helm/dapr-components/templates/pubsub-kafka.yaml
- [ ] T006 [P] Create Dapr State Store component (Redis) in helm/dapr-components/templates/statestore-redis.yaml
- [ ] T007 [P] Create Dapr Cron Binding component in helm/dapr-components/templates/binding-cron.yaml
- [ ] T008 [P] Create Dapr Secret Store component in helm/dapr-components/templates/secretstore-kubernetes.yaml
- [ ] T009 Create infrastructure setup script in scripts/setup-infra.sh

**Checkpoint**: Kafka + Dapr infrastructure ready on Minikube

---

## Phase 2: Foundational (Event Publishing in Chat API)

**Purpose**: Enable Chat API to publish task events via Dapr Pub/Sub (NO CRUD changes)

**⚠️ CRITICAL**: All downstream services depend on events from Chat API

- [ ] T010 Add @dapr/dapr dependency to services/chat-api/package.json
- [ ] T011 Create TaskEvent type definitions in services/chat-api/src/events/types.ts
- [ ] T012 [P] Create task event publisher module in services/chat-api/src/events/task-publisher.ts
- [ ] T013 [P] Create Dapr subscription endpoint in services/chat-api/src/events/subscription.ts
- [ ] T014 Integrate event publishing into task create handler (emit TaskCreated) in services/chat-api/src/events/hooks.ts
- [ ] T015 [P] Integrate event publishing into task update handler (emit TaskUpdated)
- [ ] T016 [P] Integrate event publishing into task complete handler (emit TaskCompleted)
- [ ] T017 [P] Integrate event publishing into task delete handler (emit TaskDeleted)
- [ ] T018 Add Dapr sidecar annotations to Chat API Helm chart in helm/todo-chatbot/charts/chat-api/templates/deployment.yaml
- [ ] T019 Update Chat API values with Dapr configuration in helm/todo-chatbot/charts/chat-api/values.yaml

**Checkpoint**: Chat API publishes events to Kafka via Dapr; existing CRUD unchanged

---

## Phase 3: User Story 1 - Recurring Tasks (Priority: P1) 🎯 MVP

**Goal**: Auto-create next task occurrence when recurring task is completed

**Independent Test**: Create task with RRULE, complete it, verify next occurrence created within 5 seconds

### RecurringTaskService Implementation

- [ ] T020 [US1] Initialize recurring-task-service project in services/recurring-task-service/package.json
- [ ] T021 [P] [US1] Create TypeScript config in services/recurring-task-service/tsconfig.json
- [ ] T022 [P] [US1] Create service entry point in services/recurring-task-service/src/index.ts
- [ ] T023 [US1] Create recurrence rule parser using rrule.js in services/recurring-task-service/src/services/recurrence.service.ts
- [ ] T024 [US1] Create task-completed event handler in services/recurring-task-service/src/handlers/task-completed.handler.ts
- [ ] T025 [US1] Implement next occurrence calculation logic in services/recurring-task-service/src/services/recurrence.service.ts
- [ ] T026 [US1] Implement Dapr service invocation to create new task via Chat API in services/recurring-task-service/src/services/task-creator.service.ts
- [ ] T027 [US1] Create Dapr subscription config for task-events topic in services/recurring-task-service/src/config/subscription.ts
- [ ] T028 [P] [US1] Create Dockerfile in services/recurring-task-service/Dockerfile
- [ ] T029 [US1] Create Helm chart for recurring-task-service in helm/todo-chatbot/charts/recurring-task-service/Chart.yaml
- [ ] T030 [P] [US1] Create deployment template with Dapr sidecar in helm/todo-chatbot/charts/recurring-task-service/templates/deployment.yaml
- [ ] T031 [P] [US1] Create service template in helm/todo-chatbot/charts/recurring-task-service/templates/service.yaml
- [ ] T032 [P] [US1] Create values.yaml for recurring-task-service in helm/todo-chatbot/charts/recurring-task-service/values.yaml

### Chat API Task Schema Extension (for RRULE)

- [ ] T033 [US1] Add recurrence_rule field to Task model in services/chat-api/src/models/task.ts
- [ ] T034 [US1] Create database migration for recurrence_rule column in services/chat-api/src/migrations/add-recurrence-rule.ts
- [ ] T035 [US1] Update task validation to accept RRULE strings in services/chat-api/src/validators/task.validator.ts

**Checkpoint**: Recurring tasks functional end-to-end on Minikube

---

## Phase 4: User Story 2 - Due Dates and Reminders (Priority: P1) 🎯 MVP

**Goal**: Schedule and deliver reminder notifications before task due dates

**Independent Test**: Create task with due date + reminder, wait for trigger time, verify notification delivered

### NotificationService Implementation

- [ ] T036 [US2] Initialize notification-service project in services/notification-service/package.json
- [ ] T037 [P] [US2] Create TypeScript config in services/notification-service/tsconfig.json
- [ ] T038 [P] [US2] Create service entry point in services/notification-service/src/index.ts
- [ ] T039 [US2] Create reminder scheduling service in services/notification-service/src/services/reminder.service.ts
- [ ] T040 [US2] Create task-created event handler (schedule reminder) in services/notification-service/src/handlers/task-created.handler.ts
- [ ] T041 [P] [US2] Create task-updated event handler (reschedule reminder) in services/notification-service/src/handlers/task-updated.handler.ts
- [ ] T042 [US2] Create cron trigger handler (check due reminders) in services/notification-service/src/handlers/cron-trigger.handler.ts
- [ ] T043 [US2] Implement reminder state management via Dapr State Store in services/notification-service/src/services/reminder-state.service.ts
- [ ] T044 [US2] Implement notification delivery (in-app) in services/notification-service/src/services/notification-delivery.service.ts
- [ ] T045 [US2] Create Dapr subscription config for task-events in services/notification-service/src/config/subscription.ts
- [ ] T046 [P] [US2] Create Dockerfile in services/notification-service/Dockerfile
- [ ] T047 [US2] Create Helm chart for notification-service in helm/todo-chatbot/charts/notification-service/Chart.yaml
- [ ] T048 [P] [US2] Create deployment template with Dapr sidecar in helm/todo-chatbot/charts/notification-service/templates/deployment.yaml
- [ ] T049 [P] [US2] Create service template in helm/todo-chatbot/charts/notification-service/templates/service.yaml
- [ ] T050 [P] [US2] Create values.yaml for notification-service in helm/todo-chatbot/charts/notification-service/values.yaml

### Chat API Task Schema Extension (for Due Date + Reminder)

- [ ] T051 [US2] Add due_date field to Task model in services/chat-api/src/models/task.ts
- [ ] T052 [P] [US2] Add reminder_offset field to Task model in services/chat-api/src/models/task.ts
- [ ] T053 [US2] Create database migration for due_date and reminder columns in services/chat-api/src/migrations/add-due-date-reminder.ts
- [ ] T054 [US2] Update task validation for due date and reminder in services/chat-api/src/validators/task.validator.ts

**Checkpoint**: Reminders scheduled and delivered within 1 minute of trigger time

---

## Phase 5: User Story 3 - Task Priorities (Priority: P2)

**Goal**: Allow users to assign and filter by priority levels

**Independent Test**: Create tasks with different priorities, sort/filter by priority, verify correct ordering

### Chat API Priority Implementation

- [ ] T055 [US3] Add priority enum field to Task model in services/chat-api/src/models/task.ts
- [ ] T056 [US3] Create database migration for priority column in services/chat-api/src/migrations/add-priority.ts
- [ ] T057 [US3] Update task validation for priority values in services/chat-api/src/validators/task.validator.ts
- [ ] T058 [US3] Add priority filter to task query endpoint in services/chat-api/src/controllers/task.controller.ts
- [ ] T059 [US3] Add priority sort option to task list endpoint in services/chat-api/src/controllers/task.controller.ts

**Checkpoint**: Priority filtering and sorting functional

---

## Phase 6: User Story 4 - Tags and Categorization (Priority: P2)

**Goal**: Allow users to add tags and filter tasks by tag

**Independent Test**: Create tasks with tags, filter by tag, verify correct results

### Chat API Tags Implementation

- [ ] T060 [US4] Add tags array field to Task model in services/chat-api/src/models/task.ts
- [ ] T061 [US4] Create database migration for tags column (array type) in services/chat-api/src/migrations/add-tags.ts
- [ ] T062 [US4] Add GIN index for tags array in services/chat-api/src/migrations/add-tags.ts
- [ ] T063 [US4] Update task validation for tags array in services/chat-api/src/validators/task.validator.ts
- [ ] T064 [US4] Add tag filter to task query endpoint in services/chat-api/src/controllers/task.controller.ts
- [ ] T065 [US4] Create tag autocomplete endpoint in services/chat-api/src/controllers/tag.controller.ts

**Checkpoint**: Tag filtering and autocomplete functional

---

## Phase 7: User Story 5 - Search, Filter, Sort (Priority: P2)

**Goal**: Enable keyword search and multi-criteria filtering

**Independent Test**: Create diverse tasks, search by keyword, apply multi-filter, verify results

### Chat API Search Implementation

- [ ] T066 [US5] Add full-text search index to tasks table in services/chat-api/src/migrations/add-search-index.ts
- [ ] T067 [US5] Implement keyword search endpoint in services/chat-api/src/controllers/search.controller.ts
- [ ] T068 [US5] Implement date range filter in services/chat-api/src/controllers/task.controller.ts
- [ ] T069 [US5] Implement multi-filter query builder in services/chat-api/src/services/task-query.service.ts
- [ ] T070 [US5] Implement sort options (due date, priority, created, alpha) in services/chat-api/src/services/task-query.service.ts
- [ ] T071 [US5] Add pagination to search results in services/chat-api/src/controllers/search.controller.ts

**Checkpoint**: Search returns results in < 1 second for 10K+ tasks

---

## Phase 8: User Story 6 - Audit Trail (Priority: P3)

**Goal**: Record all task changes in immutable audit log

**Independent Test**: Create/edit/complete task, query audit log, verify complete history

### AuditService Implementation

- [ ] T072 [US6] Initialize audit-service project in services/audit-service/package.json
- [ ] T073 [P] [US6] Create TypeScript config in services/audit-service/tsconfig.json
- [ ] T074 [P] [US6] Create service entry point in services/audit-service/src/index.ts
- [ ] T075 [US6] Create audit entry model in services/audit-service/src/models/audit-entry.ts
- [ ] T076 [US6] Create database migration for audit_entries table in services/audit-service/src/migrations/create-audit-entries.ts
- [ ] T077 [US6] Create task event handler (all event types) in services/audit-service/src/handlers/task-event.handler.ts
- [ ] T078 [US6] Implement audit log writer service in services/audit-service/src/services/audit-log.service.ts
- [ ] T079 [US6] Create audit query API controller in services/audit-service/src/api/audit-query.controller.ts
- [ ] T080 [US6] Implement filter by task ID, date range, action in services/audit-service/src/services/audit-query.service.ts
- [ ] T081 [US6] Create Dapr subscription config for task-events in services/audit-service/src/config/subscription.ts
- [ ] T082 [P] [US6] Create Dockerfile in services/audit-service/Dockerfile
- [ ] T083 [US6] Create Helm chart for audit-service in helm/todo-chatbot/charts/audit-service/Chart.yaml
- [ ] T084 [P] [US6] Create deployment template with Dapr sidecar in helm/todo-chatbot/charts/audit-service/templates/deployment.yaml
- [ ] T085 [P] [US6] Create service template in helm/todo-chatbot/charts/audit-service/templates/service.yaml
- [ ] T086 [P] [US6] Create values.yaml for audit-service in helm/todo-chatbot/charts/audit-service/values.yaml

**Checkpoint**: All task changes logged with before/after state

---

## Phase 9: User Story 7 - Real-Time Sync (Priority: P3)

**Goal**: Broadcast task updates to connected clients

**Independent Test**: Open app on two sessions, change task on one, verify other updates within 5 seconds

### Event Broadcasting Implementation

- [ ] T087 [US7] Create task-updates topic subscription in Chat API in services/chat-api/src/events/broadcast-subscription.ts
- [ ] T088 [US7] Implement WebSocket/SSE endpoint for client connections in services/chat-api/src/controllers/realtime.controller.ts
- [ ] T089 [US7] Implement event broadcast to connected clients in services/chat-api/src/services/realtime-broadcast.service.ts
- [ ] T090 [US7] Add connection state management in services/chat-api/src/services/connection-manager.service.ts

**Checkpoint**: Multi-device sync working within 5 seconds

---

## Phase 10: Helm Umbrella Chart & Deployment

**Purpose**: Create unified deployment for all services

- [ ] T091 Create umbrella Helm chart in helm/todo-chatbot/Chart.yaml
- [ ] T092 [P] Create default values.yaml in helm/todo-chatbot/values.yaml
- [ ] T093 [P] Create values-minikube.yaml (Strimzi Kafka, local Redis) in helm/todo-chatbot/values-minikube.yaml
- [ ] T094 [P] Create values-cloud.yaml (managed Kafka endpoint, cloud secrets) in helm/todo-chatbot/values-cloud.yaml
- [ ] T095 Add all sub-charts as dependencies in helm/todo-chatbot/Chart.yaml
- [ ] T096 Create Helm chart tests in helm/todo-chatbot/templates/tests/
- [ ] T097 Document Minikube deployment flow in docs/deployment-minikube.md
- [ ] T098 Document cloud deployment flow (AKS/GKE/OKE) in docs/deployment-cloud.md

**Checkpoint**: Single `helm upgrade` deploys entire stack

---

## Phase 11: CI/CD Pipeline (GitHub Actions)

**Purpose**: Automate build, test, and deployment

- [ ] T099 Create CI workflow (lint, test) in .github/workflows/ci.yaml
- [ ] T100 [P] Create Docker image build workflow in .github/workflows/build-images.yaml
- [ ] T101 [P] Create Minikube deployment verification workflow in .github/workflows/deploy-minikube.yaml
- [ ] T102 Create cloud deployment workflow (manual trigger) in .github/workflows/deploy-cloud.yaml
- [ ] T103 Configure GitHub secrets for container registry in .github/workflows/build-images.yaml
- [ ] T104 Configure GitHub secrets for Kubernetes cluster access in .github/workflows/deploy-cloud.yaml

**Checkpoint**: PRs trigger CI; merges to main build images; manual dispatch deploys

---

## Phase 12: Polish & Cross-Cutting Concerns

**Purpose**: Observability, documentation, and quality assurance

- [ ] T105 Configure Dapr observability (tracing, metrics) in helm/dapr-components/templates/observability.yaml
- [ ] T106 [P] Add structured logging to recurring-task-service in services/recurring-task-service/src/utils/logger.ts
- [ ] T107 [P] Add structured logging to notification-service in services/notification-service/src/utils/logger.ts
- [ ] T108 [P] Add structured logging to audit-service in services/audit-service/src/utils/logger.ts
- [ ] T109 Create health check endpoints for all new services
- [ ] T110 Update project README with Phase 5 architecture in README.md
- [ ] T111 Create operational runbook in docs/runbook.md
- [ ] T112 Verify end-to-end flow on Minikube (all user stories)
- [ ] T113 Verify Helm chart works with cloud values (managed Kafka)

**Checkpoint**: Production-ready with monitoring and documentation

---

## Dependencies

### User Story Completion Order

```
Phase 1 (Setup) ─────────────────────────────────────────────────────┐
     │                                                                │
Phase 2 (Chat API Events) ───────────────────────────────────────────┤
     │                                                                │
     ├── Phase 3 (US1: Recurring Tasks) ─── MVP DELIVERABLE ──────────┤
     │                                                                │
     ├── Phase 4 (US2: Reminders) ─── MVP DELIVERABLE ────────────────┤
     │                                                                │
     ├── Phase 5 (US3: Priorities) ───────────────────────────────────┤
     │       │                                                        │
     │       └── Phase 7 (US5: Search) depends on priorities ─────────┤
     │                                                                │
     ├── Phase 6 (US4: Tags) ─────────────────────────────────────────┤
     │       │                                                        │
     │       └── Phase 7 (US5: Search) depends on tags ───────────────┤
     │                                                                │
     ├── Phase 8 (US6: Audit) ── independent, consumes events ────────┤
     │                                                                │
     └── Phase 9 (US7: Real-time) ── independent, uses events ────────┤
                                                                      │
Phase 10-11 (Helm + CI/CD) ───────────────────────────────────────────┤
     │                                                                │
Phase 12 (Polish) ────────────────────────────────────────────────────┘
```

### Parallel Execution Opportunities

**Within Phase 1 (Infrastructure)**:
- T002, T003 (Kafka manifests) can run parallel
- T005, T006, T007, T008 (Dapr components) can run parallel

**Within Phase 2 (Event Publishing)**:
- T012, T013 (event modules) can run parallel
- T015, T016, T017 (event hooks) can run parallel

**Within Phase 3 (US1)**:
- T021, T022 (config files) can run parallel
- T028, T030, T031, T032 (Helm/Docker) can run parallel

**Within Phase 4 (US2)**:
- T037, T038 (config files) can run parallel
- T046, T048, T049, T050 (Helm/Docker) can run parallel

**Cross-Phase Parallelism**:
- US3, US4, US5 can run in parallel after Phase 2 completes
- US6 (Audit) can run in parallel with US3-US5
- US7 (Real-time) can run in parallel with US6

---

## Implementation Strategy

### MVP Scope (Phases 1-4)
1. **Phase 1**: Infrastructure (Kafka, Dapr, Redis) on Minikube
2. **Phase 2**: Chat API event publishing
3. **Phase 3**: Recurring tasks (US1) - core differentiator
4. **Phase 4**: Due dates and reminders (US2) - essential UX

**MVP Deliverable**: Users can create recurring tasks and receive reminders

### Post-MVP (Phases 5-12)
5. **Phases 5-7**: Task organization (priorities, tags, search)
6. **Phase 8**: Audit trail for compliance
7. **Phase 9**: Real-time sync for multi-device
8. **Phases 10-11**: Production deployment and CI/CD
9. **Phase 12**: Polish and documentation

---

## Summary

| Category | Count |
|----------|-------|
| Total Tasks | 113 |
| Setup Tasks (Phase 1) | 9 |
| Foundational Tasks (Phase 2) | 10 |
| US1 (Recurring) Tasks | 16 |
| US2 (Reminders) Tasks | 19 |
| US3 (Priorities) Tasks | 5 |
| US4 (Tags) Tasks | 6 |
| US5 (Search) Tasks | 6 |
| US6 (Audit) Tasks | 15 |
| US7 (Real-time) Tasks | 4 |
| Helm/Deployment Tasks | 8 |
| CI/CD Tasks | 6 |
| Polish Tasks | 9 |
| Parallelizable [P] Tasks | 42 |

### MVP Task Count: 54 tasks (Phases 1-4)
### Post-MVP Task Count: 59 tasks (Phases 5-12)
