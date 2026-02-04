---
id: 003
title: Phase 5 Implementation Plan
stage: plan
date: 2026-01-30
surface: agent
model: claude-sonnet-4-5-20250929
feature: 1-event-driven-microservices
branch: main
user: user
command: /sp.plan
labels: ["planning", "architecture", "dapr", "kafka", "microservices", "helm", "kubernetes"]
links:
  spec: specs/1-event-driven-microservices/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/1-event-driven-microservices/plan.md
  - specs/1-event-driven-microservices/research.md
  - specs/1-event-driven-microservices/data-model.md
  - specs/1-event-driven-microservices/quickstart.md
  - specs/1-event-driven-microservices/contracts/task-events.schema.json
  - specs/1-event-driven-microservices/contracts/reminder-events.schema.json
  - specs/1-event-driven-microservices/contracts/audit-api.openapi.yaml
tests:
  - none
---

## Prompt

Create an execution plan for Phase 5.

Start from Phase 4 Helm-based Kubernetes deployment.

Add:
- Kafka cluster in Kubernetes (local via Strimzi)
- Dapr installation and components
- Event publishing in existing Chat API via Dapr Pub/Sub
- New microservices:
  - recurring-task-service
  - notification-service
  - audit-service
- Helm charts for each new service
- Dapr sidecar injection for all pods
- Local Minikube deployment flow
- Cloud deployment flow to AKS/GKE/OKE
- Switching Pub/Sub from local Kafka to managed Kafka without code change
- GitHub Actions CI/CD to build images and deploy with Helm
- Basic monitoring/logging setup

Do not modify existing CRUD or AI agent logic.

## Response snapshot

Created comprehensive implementation plan with Phase 0 (Research) and Phase 1 (Design) artifacts:

**plan.md** - Main implementation plan including:
- Technical context (TypeScript/Node.js 20, Dapr 1.12+, Kafka 3.x, Helm 3.x)
- Constitution compliance check (all 7 principles pass)
- Project structure (services/, helm/, .github/workflows/, tests/)
- 9 implementation stages with 51 tasks
- Deployment flows for Minikube and cloud (AKS/GKE/OKE)
- Risk mitigations (event ordering, Kafka availability, clock skew)
- ADR suggestions for CloudEvents format, Strimzi, and Helm structure

**research.md** - Technology decisions:
- Dapr Pub/Sub with Kafka (abstraction, portability, built-in features)
- Strimzi Kafka Operator (Kubernetes-native, CRD-based)
- rrule.js for iCalendar RRULE parsing
- Dapr Cron Bindings for scheduled reminders
- CloudEvents v1.0 for event schema versioning

**data-model.md** - Entity schemas:
- Task (enhanced with due_date, priority, tags, recurrence_rule)
- Reminder (Dapr State Store - Redis)
- AuditEntry (PostgreSQL)
- State transitions and relationships
- Database migrations

**contracts/** - Event schemas and API definitions:
- task-events.schema.json (CloudEvents format)
- reminder-events.schema.json
- audit-api.openapi.yaml (OpenAPI 3.1)

**quickstart.md** - Local development setup:
- Minikube configuration (4 CPU, 8GB RAM)
- Dapr, Strimzi, Redis installation
- Service deployment and access
- Testing the event flow
- Troubleshooting guide

## Outcome

- ✅ **Impact**: Complete implementation blueprint; all 7 constitution principles verified; ready for task generation.
- 🧪 **Tests**: Contract schemas (JSON Schema, OpenAPI) provide validation baseline; 51 implementation tasks outlined.
- 📁 **Files**: 7 artifacts created in specs/1-event-driven-microservices/
- 🔁 **Next prompts**: Run `/sp.tasks` to generate actionable task list; Consider `/sp.adr event-schema-format` for CloudEvents decision.
- 🧠 **Reflection**: Plan maintains strict separation from Phase 4 code; all new functionality is additive via event publishing. Dapr abstraction ensures Minikube-to-cloud portability. Umbrella Helm chart simplifies deployment while preserving service independence.

## Evaluation notes (flywheel)

- **Failure modes observed**: None; all constitution gates passed.
- **Graders run and results (PASS/FAIL)**: Constitution compliance check - PASS (7/7 principles).
- **Prompt variant (if applicable)**: None.
- **Next experiment**: Validate Strimzi resource limits on constrained Minikube; test Dapr Pub/Sub retry behavior under Kafka partition rebalancing.
