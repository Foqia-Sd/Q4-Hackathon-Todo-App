# Implementation Plan: Phase 5 Event-Driven Microservices

**Branch**: `1-event-driven-microservices` | **Date**: 2026-01-30 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/1-event-driven-microservices/spec.md`

## Summary

Extend the Phase 4 Kubernetes Todo Chatbot with event-driven microservices architecture using Dapr and Kafka. Add three new microservices (RecurringTaskService, NotificationService, AuditService) that consume task events published by the existing Chat API. Enable recurring tasks, due-date reminders, and activity audit logging without modifying existing CRUD logic. Deploy via Helm charts to both Minikube (self-hosted Kafka via Strimzi) and cloud Kubernetes (managed Kafka) with zero code changes between environments.

## Technical Context

**Language/Version**: TypeScript 5.x / Node.js 20 LTS (matching Phase 4 Chat API)
**Primary Dependencies**:
- Dapr SDK for Node.js (@dapr/dapr)
- Express.js (HTTP endpoints for Dapr subscriptions)
- date-fns or luxon (date/time handling for recurrence and reminders)
- rrule (iCalendar RRULE parsing for recurrence patterns)

**Infrastructure**:
- Kubernetes 1.28+ (Minikube 1.30+ local, AKS/GKE/OKE cloud)
- Dapr 1.12+ (sidecar injection, Pub/Sub, State Store, Bindings, Secrets)
- Kafka 3.x via Strimzi Operator (local) or managed Kafka/Redpanda (cloud)
- Helm 3.x for all deployments

**Storage**:
- PostgreSQL (existing Phase 4 database for domain data)
- Dapr State Store backed by Redis (service-specific state: recurrence tracking, reminder scheduling)

**Testing**:
- Jest (unit tests)
- Supertest (HTTP integration tests)
- Dapr test containers (local Pub/Sub verification)
- Helm chart linting and template validation

**Target Platform**: Kubernetes (Minikube local, AKS/GKE/OKE cloud)
**Project Type**: Microservices (multiple independently deployable services)
**Performance Goals**:
- Event processing latency < 5 seconds (recurring task creation)
- Reminder delivery within 1 minute of scheduled time
- Search/filter response < 1 second for 10K+ tasks

**Constraints**:
- Zero modifications to existing Phase 4 Chat API business logic
- All external access via Dapr sidecars (no direct Kafka/Redis/DB clients)
- Stateless services; all state persisted to Dapr State Store or database
- Environment portability: same Helm charts for Minikube and cloud

**Scale/Scope**:
- 1,000 concurrent users
- 100,000+ tasks across all users
- 3 new microservices + Dapr components + CI/CD pipelines

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Evidence |
|-----------|--------|----------|
| I. Preserve Existing Functionality | ✅ PASS | No modifications to Phase 4 Chat API CRUD logic; new services are additive |
| II. Event-Driven Microservices | ✅ PASS | All new services communicate via Dapr Pub/Sub; loosely coupled design |
| III. Dapr-First External Access | ✅ PASS | No direct Kafka clients; Dapr Pub/Sub, State Store, Bindings, Secrets only |
| IV. Infrastructure as Code & Helm | ✅ PASS | All services deployed via Helm charts with environment-specific values |
| V. CI/CD via GitHub Actions | ✅ PASS | GitHub Actions workflows for build, test, image push, Helm deploy |
| VI. Stateless Services | ✅ PASS | Services persist state to Dapr State Store (Redis) or PostgreSQL |
| VII. Domain-Driven Event Publishing | ✅ PASS | Chat API is sole publisher; new services are consumers only |

**Violations**: None. All principles satisfied by design.

## Project Structure

### Documentation (this feature)

```text
specs/1-event-driven-microservices/
├── plan.md              # This file
├── research.md          # Phase 0: Technology decisions and patterns
├── data-model.md        # Phase 1: Entity schemas and relationships
├── quickstart.md        # Phase 1: Local development setup
├── contracts/           # Phase 1: Event schemas, API contracts
│   ├── task-events.schema.json
│   ├── reminder-events.schema.json
│   └── audit-api.openapi.yaml
├── checklists/
│   └── requirements.md  # Spec quality validation
└── tasks.md             # Phase 2 output (created by /sp.tasks)
```

### Source Code (repository root)

```text
# Microservices Architecture
services/
├── chat-api/                    # Existing Phase 4 service (UNCHANGED)
│   ├── src/
│   │   ├── events/              # NEW: Event publishing module
│   │   │   └── task-publisher.ts
│   │   └── ... (existing code unchanged)
│   ├── Dockerfile
│   └── package.json
│
├── recurring-task-service/      # NEW: Microservice
│   ├── src/
│   │   ├── handlers/
│   │   │   └── task-completed.handler.ts
│   │   ├── services/
│   │   │   └── recurrence.service.ts
│   │   └── index.ts
│   ├── Dockerfile
│   ├── package.json
│   └── tsconfig.json
│
├── notification-service/        # NEW: Microservice
│   ├── src/
│   │   ├── handlers/
│   │   │   ├── task-created.handler.ts
│   │   │   └── cron-trigger.handler.ts
│   │   ├── services/
│   │   │   └── reminder.service.ts
│   │   └── index.ts
│   ├── Dockerfile
│   ├── package.json
│   └── tsconfig.json
│
└── audit-service/               # NEW: Microservice
    ├── src/
    │   ├── handlers/
    │   │   └── task-event.handler.ts
    │   ├── services/
    │   │   └── audit-log.service.ts
    │   ├── api/
    │   │   └── audit-query.controller.ts
    │   └── index.ts
    ├── Dockerfile
    ├── package.json
    └── tsconfig.json

# Helm Charts
helm/
├── todo-chatbot/                # Umbrella chart
│   ├── Chart.yaml
│   ├── values.yaml              # Default values
│   ├── values-minikube.yaml     # Local Minikube overrides
│   ├── values-cloud.yaml        # Cloud (AKS/GKE/OKE) overrides
│   └── charts/
│       ├── chat-api/
│       ├── recurring-task-service/
│       ├── notification-service/
│       ├── audit-service/
│       └── dapr-components/
│
├── strimzi-kafka/               # Kafka cluster for local development
│   ├── Chart.yaml
│   └── templates/
│       ├── kafka-cluster.yaml
│       └── kafka-topics.yaml
│
└── dapr-components/             # Shared Dapr component definitions
    ├── Chart.yaml
    └── templates/
        ├── pubsub-kafka.yaml
        ├── statestore-redis.yaml
        ├── binding-cron.yaml
        └── secretstore-kubernetes.yaml

# CI/CD
.github/
└── workflows/
    ├── ci.yaml                  # Build, lint, test on PR
    ├── build-images.yaml        # Build and push Docker images
    ├── deploy-minikube.yaml     # Local deployment verification
    └── deploy-cloud.yaml        # Cloud deployment (manual trigger)

# Tests
tests/
├── contract/                    # Event schema validation
├── integration/                 # Cross-service tests with Dapr
└── e2e/                         # End-to-end workflows
```

**Structure Decision**: Microservices architecture with each service as an independent deployable unit. Umbrella Helm chart manages all services and Dapr components. Strimzi Kafka chart provides local message broker.

## Complexity Tracking

> No violations. All design choices align with constitution principles.

| Aspect | Decision | Justification |
|--------|----------|---------------|
| 3 new microservices | Required | Constitution mandates separate services for new capabilities |
| Umbrella Helm chart | Simplifies deployment | Single `helm upgrade` deploys entire stack; sub-charts remain independent |
| Strimzi for local Kafka | Best practice | Kubernetes-native Kafka operator; production-like local environment |
| Redis for State Store | Dapr recommended | Fast, ephemeral state; not domain data (goes to PostgreSQL) |

---

## Phase 0: Research & Technology Decisions

### Research Areas

1. **Dapr Pub/Sub with Kafka**: Configuration patterns, message ordering, dead-letter topics
2. **Strimzi Kafka Operator**: Minikube deployment, resource limits, topic management
3. **iCalendar RRULE**: Library selection (rrule.js), edge cases (month-end dates)
4. **Dapr Cron Bindings**: Syntax, timezone handling, trigger reliability
5. **Event Schema Versioning**: CloudEvents format, backward compatibility

### Decisions (to be detailed in research.md)

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Event Format | CloudEvents v1.0 | Industry standard; Dapr native support; extensible metadata |
| Recurrence Library | rrule.js | Full RFC 5545 support; well-maintained; TypeScript types |
| Kafka Deployment (local) | Strimzi 0.38+ | Kubernetes-native; CRD-based; production parity |
| Kafka Deployment (cloud) | Managed (Redpanda/Confluent) | Zero ops burden; Dapr Pub/Sub abstraction unchanged |
| State Store Backend | Redis (Dapr component) | Fast ephemeral state; service-specific; not domain data |
| Secrets Management | Kubernetes Secrets via Dapr | Native K8s integration; works Minikube and cloud |

---

## Phase 1: Design & Contracts

### Data Model (to be detailed in data-model.md)

#### Enhanced Task Entity (Chat API Database)

```
Task (existing + new fields)
├── id: UUID (PK)
├── title: string
├── description: string (nullable)
├── completed: boolean
├── created_at: timestamp
├── updated_at: timestamp
├── user_id: UUID (FK)
│
├── due_date: timestamp (nullable)       # NEW
├── priority: enum (HIGH|MEDIUM|LOW|NONE) # NEW
├── tags: string[] (array)               # NEW
└── recurrence_rule: string (RRULE, nullable) # NEW
```

#### Reminder Entity (Notification Service State Store)

```
Reminder
├── id: UUID (PK)
├── task_id: UUID (FK)
├── user_id: UUID
├── trigger_time: timestamp
├── reminder_offset: string (e.g., "PT1H", "P1D")
├── status: enum (PENDING|SENT|CANCELLED)
└── created_at: timestamp
```

#### AuditEntry Entity (Audit Service Database)

```
AuditEntry
├── id: UUID (PK)
├── task_id: UUID
├── user_id: UUID
├── action: enum (CREATED|UPDATED|COMPLETED|DELETED)
├── timestamp: timestamp
├── before_state: JSONB (nullable)
├── after_state: JSONB
└── metadata: JSONB (actor, source, correlation_id)
```

### Event Contracts (to be detailed in contracts/)

#### TaskEvent (CloudEvents format)

```json
{
  "specversion": "1.0",
  "type": "com.todo.task.created|updated|completed|deleted",
  "source": "/services/chat-api",
  "id": "<uuid>",
  "time": "<ISO8601>",
  "datacontenttype": "application/json",
  "data": {
    "taskId": "<uuid>",
    "userId": "<uuid>",
    "action": "CREATED|UPDATED|COMPLETED|DELETED",
    "task": { /* full task snapshot */ },
    "changes": { /* diff for UPDATED action */ },
    "correlationId": "<uuid>"
  }
}
```

#### Kafka Topics

| Topic | Publishers | Consumers | Purpose |
|-------|------------|-----------|---------|
| `task-events` | Chat API | RecurringTaskService, AuditService | All task lifecycle events |
| `task-reminders` | NotificationService | NotificationService | Scheduled reminder triggers |
| `task-updates` | Chat API | Clients (WebSocket/SSE) | Real-time sync |

### Dapr Component Configuration

#### Pub/Sub (Kafka)

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: task-pubsub
spec:
  type: pubsub.kafka
  version: v1
  metadata:
    - name: brokers
      value: "kafka-cluster-kafka-bootstrap:9092"  # Minikube
      # value: "<managed-kafka-broker>:9092"       # Cloud (values override)
    - name: consumerGroup
      value: "{appId}-group"
    - name: authType
      value: "none"  # Minikube
      # value: "mtls"  # Cloud (values override)
```

#### State Store (Redis)

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
spec:
  type: state.redis
  version: v1
  metadata:
    - name: redisHost
      value: "redis-master:6379"
    - name: redisPassword
      secretKeyRef:
        name: redis-secret
        key: password
```

#### Cron Binding (Reminder Trigger)

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: reminder-cron
spec:
  type: bindings.cron
  version: v1
  metadata:
    - name: schedule
      value: "*/1 * * * *"  # Every minute
    - name: route
      value: "/check-reminders"
```

---

## Phase 2: Implementation Sequence

> **Note**: Detailed tasks will be generated by `/sp.tasks` command.

### Stage 1: Infrastructure Foundation
1. Install Dapr on Minikube cluster
2. Deploy Strimzi Kafka operator and cluster
3. Create Kafka topics (task-events, task-reminders, task-updates)
4. Deploy Redis for Dapr State Store
5. Configure Dapr components (Pub/Sub, State Store, Secrets)

### Stage 2: Chat API Event Publishing
6. Add event publishing module to Chat API (no CRUD changes)
7. Publish TaskCreated event on task creation
8. Publish TaskUpdated event on task update
9. Publish TaskCompleted event on task completion
10. Publish TaskDeleted event on task deletion
11. Add Dapr sidecar annotation to Chat API Helm chart

### Stage 3: Recurring Task Service
12. Create service scaffold (Express + Dapr SDK)
13. Implement TaskCompleted event handler
14. Implement recurrence rule parser (rrule.js)
15. Implement next occurrence calculation
16. Publish new task via Dapr Service Invocation to Chat API
17. Create Helm chart with Dapr sidecar injection
18. Write unit and integration tests

### Stage 4: Notification Service
19. Create service scaffold (Express + Dapr SDK)
20. Implement TaskCreated/TaskUpdated event handlers
21. Implement reminder scheduling logic
22. Store scheduled reminders in Dapr State Store
23. Implement cron binding handler for reminder checks
24. Implement reminder delivery (in-app notification)
25. Create Helm chart with Dapr sidecar injection
26. Write unit and integration tests

### Stage 5: Audit Service
27. Create service scaffold (Express + Dapr SDK)
28. Implement TaskEvent handler (all event types)
29. Create audit_entries table in PostgreSQL
30. Implement audit log writer
31. Implement audit query API (filter by task, date, action)
32. Create Helm chart with Dapr sidecar injection
33. Write unit and integration tests

### Stage 6: Task Enhancements (Chat API)
34. Add due_date field to Task model
35. Add priority field to Task model
36. Add tags field to Task model
37. Add recurrence_rule field to Task model
38. Implement search endpoint (keyword search)
39. Implement filter endpoint (due date, priority, tags, status)
40. Implement sort options (due date, priority, created, alpha)
41. Write unit and integration tests

### Stage 7: Helm & Deployment
42. Create umbrella Helm chart
43. Create values-minikube.yaml with Strimzi Kafka config
44. Create values-cloud.yaml with managed Kafka config
45. Test deployment on Minikube
46. Document cloud deployment (AKS/GKE/OKE)

### Stage 8: CI/CD Pipeline
47. Create GitHub Actions workflow for CI (lint, test)
48. Create GitHub Actions workflow for Docker image builds
49. Create GitHub Actions workflow for Helm deployment
50. Configure secrets for container registry and K8s cluster

### Stage 9: Monitoring & Observability
51. Configure Dapr observability (tracing, metrics)
52. Add structured logging to all services
53. Create basic Grafana dashboard (optional)
54. Document operational runbooks

---

## Deployment Flows

### Local (Minikube)

```bash
# 1. Start Minikube with sufficient resources
minikube start --cpus=4 --memory=8192 --driver=docker

# 2. Install Dapr
dapr init -k

# 3. Install Strimzi Kafka Operator
helm repo add strimzi https://strimzi.io/charts/
helm install strimzi-kafka-operator strimzi/strimzi-kafka-operator

# 4. Deploy Kafka cluster and topics
helm install kafka ./helm/strimzi-kafka -f ./helm/strimzi-kafka/values-minikube.yaml

# 5. Deploy Redis
helm install redis bitnami/redis --set auth.enabled=false

# 6. Deploy application stack
helm install todo-chatbot ./helm/todo-chatbot -f ./helm/todo-chatbot/values-minikube.yaml

# 7. Verify
kubectl get pods -l app.kubernetes.io/part-of=todo-chatbot
dapr dashboard -k
```

### Cloud (AKS/GKE/OKE)

```bash
# 1. Connect to cluster
az aks get-credentials --name <cluster> --resource-group <rg>  # AKS
# gcloud container clusters get-credentials <cluster>          # GKE
# oci ce cluster create-kubeconfig --cluster-id <id>           # OKE

# 2. Install Dapr
dapr init -k --enable-mtls

# 3. Configure managed Kafka connection (via values-cloud.yaml)
# - Update brokers endpoint
# - Configure mTLS or SASL auth

# 4. Deploy application stack (same Helm chart, different values)
helm install todo-chatbot ./helm/todo-chatbot -f ./helm/todo-chatbot/values-cloud.yaml

# 5. Verify
kubectl get pods -l app.kubernetes.io/part-of=todo-chatbot
```

**Key Insight**: The only difference between local and cloud deployment is the values file. Application code and Helm charts are identical.

---

## Risk Mitigations

| Risk | Mitigation | Validation |
|------|------------|------------|
| Event ordering issues | Include sequence numbers in events; idempotent handlers | Integration test with concurrent events |
| Kafka unavailability | Dapr retry policies; graceful degradation in UI | Chaos test: kill Kafka pods |
| Clock skew for reminders | UTC timestamps; ±1 minute tolerance | Test with NTP drift simulation |
| Chat API changes break events | Event schema versioning; contract tests | CI contract validation |
| Dapr sidecar injection fails | Explicit annotations; health checks | Smoke test in CI |

---

## Next Steps

1. **Generate research.md**: Run Phase 0 research on Dapr Pub/Sub, Strimzi, rrule.js
2. **Generate data-model.md**: Finalize entity schemas from design above
3. **Generate contracts/**: Create JSON Schema and OpenAPI files
4. **Generate quickstart.md**: Local development setup guide
5. **Run /sp.tasks**: Generate actionable task list from this plan

---

## Appendix: ADR Suggestions

📋 **Architectural decision detected**: CloudEvents format for task events
Document reasoning and tradeoffs? Run `/sp.adr event-schema-format`

📋 **Architectural decision detected**: Strimzi for local Kafka deployment
Document reasoning and tradeoffs? Run `/sp.adr local-kafka-strategy`

📋 **Architectural decision detected**: Umbrella Helm chart pattern
Document reasoning and tradeoffs? Run `/sp.adr helm-chart-structure`
