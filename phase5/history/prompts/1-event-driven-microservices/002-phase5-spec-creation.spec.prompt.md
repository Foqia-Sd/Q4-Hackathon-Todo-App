---
id: 002
title: Phase 5 Spec Creation
stage: spec
date: 2026-01-30
surface: agent
model: claude-sonnet-4-5-20250929
feature: 1-event-driven-microservices
branch: main
user: user
command: /sp.specify
labels: ["specification", "event-driven", "microservices", "recurring-tasks", "reminders", "dapr"]
links:
  spec: specs/1-event-driven-microservices/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/1-event-driven-microservices/spec.md
  - specs/1-event-driven-microservices/checklists/requirements.md
tests:
  - none
---

## Prompt

Specify Phase 5 advanced functionality for the Todo Chatbot.

Features to add:
1. Recurring tasks
2. Due dates and reminders
3. Priorities, tags, search, filter, sort
4. Event-driven architecture using Kafka topics:
   - task-events
   - reminders
   - task-updates
5. Separate microservices:
   - RecurringTaskService (consumes task-events)
   - NotificationService (consumes reminders)
   - AuditService (consumes task-events and stores history)
6. Real-time sync via events (task-updates)
Use Dapr:
- Pub/Sub backed by Kafka
- State store for conversation/task metadata if needed
- Cron binding for scheduled reminder triggers
- Service invocation between services
- Secrets for credentials

Deployment requirements:
- Works locally on Minikube with self-hosted Kafka
- Works in cloud (AKS/GKE/OKE) with managed Kafka (e.g. Redpanda)
- Helm charts for all services
- No changes to existing frontend/backend APIs

Non-goals:
- No UI redesign
- No changes to existing CRUD endpoints

## Response snapshot

Created comprehensive feature specification for Phase 5 Event-Driven Microservices:

**User Stories (7 total, prioritized)**:
- P1: Recurring Tasks, Due Dates & Reminders (core functionality)
- P2: Priorities, Tags, Search/Filter/Sort (organization features)
- P3: Audit Trail, Real-Time Sync (advanced features)

**Functional Requirements (24 total)**:
- FR-001 to FR-010: Task enhancements (recurrence, due dates, reminders, priorities, tags, search/filter/sort)
- FR-011 to FR-020: Event-driven architecture (Pub/Sub, Dapr building blocks)
- FR-021 to FR-024: Deployment & operations (Helm, Minikube, cloud K8s)

**Success Criteria (10 measurable outcomes)**:
- Recurring task creation within 5 seconds
- Reminder delivery within 1 minute (99% reliability)
- Search results in under 1 second for 10K+ tasks
- Real-time sync within 5 seconds
- Zero breaking changes to existing APIs

**Key Entities**: Task (enhanced), RecurrenceRule, Reminder, AuditEntry, Tag, TaskEvent

**Edge Cases**: 6 documented with resolution strategies

**Files Created**:
- `specs/1-event-driven-microservices/spec.md` (comprehensive specification)
- `specs/1-event-driven-microservices/checklists/requirements.md` (quality validation)

## Outcome

- ✅ **Impact**: Complete specification ready for planning phase; all requirements testable and measurable; no implementation details leaked.
- 🧪 **Tests**: 10 success criteria define acceptance thresholds; all user stories have Given/When/Then scenarios.
- 📁 **Files**: spec.md (main specification), checklists/requirements.md (validation checklist)
- 🔁 **Next prompts**: Run `/sp.clarify` if questions exist; Run `/sp.plan` to create implementation plan; Consider ADR for event schema design.
- 🧠 **Reflection**: Made informed decisions on defaults (iCalendar RRULE for recurrence, fixed priority levels, in-app notifications only) rather than requesting clarification. Kept spec technology-agnostic while referencing Dapr building blocks as architectural contracts.

## Evaluation notes (flywheel)

- **Failure modes observed**: None; all checklist items passed on first iteration.
- **Graders run and results (PASS/FAIL)**: Requirements checklist - PASS (all 16 items verified).
- **Prompt variant (if applicable)**: None.
- **Next experiment**: Validate spec against Phase 4 codebase structure to ensure extension points exist; consider ADR for event schema versioning strategy.
