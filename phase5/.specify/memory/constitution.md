# Phase 5: AI-Powered Todo Chatbot Constitution

<!-- Sync Impact Report: v1.0.0 → v1.0.0 (New Constitution) | Created 2026-01-30 -->

## Core Principles

### I. Preserve Existing Functionality
No refactoring of existing Phase 3/4 business logic. All CRUD operations, AI chat functionality, and Kubernetes deployments remain unchanged. New capabilities must be added as separate, independent services without modifying legacy code paths.

**Rationale:** Minimize risk of regression; enable parallel development of new features; maintain stability of proven functionality.

### II. Event-Driven Microservices Architecture
New services communicate exclusively via Dapr Pub/Sub backed by Kafka. Services are loosely coupled, stateless, and consume events published by the Chat API and other domain services.

**Rationale:** Enables scalability, resilience, and independent team deployment; decouples task creation from side effects (reminders, recurrence, audit); allows services to be added/removed without redeploying core.

### III. Dapr-First External Access
All communication with external systems (Kafka, databases, secrets, cron bindings) must route through Dapr sidecars. No direct client libraries for Kafka, database connectors, or secrets management. Dapr abstracts infrastructure and ensures cloud portability.

**Rationale:** Enables seamless migration from Minikube to Oracle Cloud without code changes; centralizes observability; simplifies secrets rotation and credential management; enforces consistent timeout and retry semantics.

### IV. Infrastructure as Code & Helm Deployment
All services and infrastructure must be deployed via Helm charts. Charts must be environment-agnostic (Minikube, Oracle Cloud, or any Kubernetes cluster) and parameterized via `values.yaml`. No manual deployments or imperative kubectl commands in production workflows.

**Rationale:** Reproducible, auditable deployments; single source of truth for cluster state; enables GitOps workflows; simplifies rollbacks and upgrades.

### V. CI/CD via GitHub Actions
All builds, tests, and deployments are orchestrated through GitHub Actions workflows. Workflows trigger on commit/PR and enforce passing tests before merge. Container images are built and pushed automatically; Helm deployments are triggered by GitOps or manual workflow dispatch.

**Rationale:** Auditable change history; automated enforcement of quality gates; consistent build environment; enables multi-environment deployments (dev, staging, prod).

### VI. Stateless Services & Persistent State via Dapr State Store or Database
Services must not retain mutable state in memory or local filesystem. All persistence goes through Dapr State Store (for service-specific state) or the shared database (for domain data). This ensures services can be scaled horizontally and replaced without data loss.

**Rationale:** Enables true statelessness and horizontal scaling; simplifies debugging and state migration; allows service restarts without user impact.

### VII. Domain-Driven Event Publishing
The Chat API (core task CRUD) is the authoritative publisher of task lifecycle events (Created, Updated, Completed, Deleted, Recurrence Triggered). Specialized services subscribe and react without feedback loops. Events include immutable task snapshots and metadata to prevent version skew.

**Rationale:** Clear ownership of event generation; prevents circular event flows; ensures all state changes are auditable; simplifies consumer logic (no polling or state reconciliation).

## Event-Driven Services

### Recurring Task Service
**Responsibility:** Consumes TaskCreated and TaskUpdated events with recurrence rules. Automatically creates next occurrence when previous is marked complete or when cron binding triggers.

**Dapr Building Blocks:** Pub/Sub (consume events), State Store (track recurrence state), Bindings (cron triggers).

### Notification Service
**Responsibility:** Consumes task events (Created, Updated, DueDate changed). Schedules and sends reminders asynchronously (email, in-app, SMS if configured). Respects user notification preferences via Dapr Secrets.

**Dapr Building Blocks:** Pub/Sub (consume events), Bindings (scheduled reminders), Service Invocation (call auth service for user prefs).

### Audit/Activity Service
**Responsibility:** Consumes all task and user action events. Writes immutable audit log to database. Provides read-only API for compliance and debugging. No event publishing; pure sink.

**Dapr Building Blocks:** Pub/Sub (consume events), State Store (temporary buffering), direct database writes (immutable append).

## External System Access Rules

- **Kafka:** Accessed only via Dapr Pub/Sub; no KafkaProducer or KafkaConsumer clients in application code.
- **Database:** Accessed via Dapr State Store for service-specific state; direct connection (with Dapr secret mgmt) for domain/audit tables.
- **Secrets (API keys, DB credentials):** Loaded via Dapr Secrets building block; never hardcoded or read from environment directly.
- **Cron/Timers:** Defined as Dapr Bindings (cron trigger) in Helm values; no K8s CronJobs or in-app schedulers.
- **Service-to-Service Calls:** Use Dapr Service Invocation (with mutual TLS); no direct HTTP/gRPC between pods.

## Deployment & Environment Portability

**Helm Chart Structure:**
- `chat-api/` — Core task service (unchanged from Phase 4)
- `recurring-task-service/` — New microservice
- `notification-service/` — New microservice
- `audit-service/` — New microservice
- `dapr-components/` — Dapr configuration (Pub/Sub, State Store, Bindings, Secrets)

**Environment Values:**
- `values-minikube.yaml` — Local Minikube with in-cluster Kafka, SQLite/PostgreSQL
- `values-oracle-cloud.yaml` — Oracle Cloud with managed services (Kafka, Autonomous DB, Vault)
- Single codebase; no conditional compilation or feature flags for environment.

**Testing:** All services must run on Minikube first. Integration tests verify Dapr contracts. Production deployment on Oracle Cloud uses identical Helm charts with environment-specific values only.

## Success Criteria & Acceptance Tests

- ✅ **Recurring Tasks:** New occurrence auto-created within 5 seconds of task completion or cron trigger. No manual intervention.
- ✅ **Due-Date Reminders:** Notification published within 1 minute of due date. Delivery method respects user preference (async, no blocking).
- ✅ **Event Audit Log:** Every task state change logged with timestamp, actor, old/new state. Queries support filtering by task ID, date range, action type.
- ✅ **Helm Portability:** `helm upgrade` on Minikube and Oracle Cloud with same chart; only values.yaml differs. No code rebuild required.
- ✅ **CI/CD Automation:** All commits to `main` build container images, run tests, publish to registry. Staging/prod deployments triggered by workflow or manual dispatch.
- ✅ **Zero Breaking Changes:** Phase 3/4 Chat API endpoints unchanged. Existing clients continue to work. New features accessible via new event subscriptions only.

## Constraints & Non-Negotiables

- No direct Kafka clients or libraries in application code (Dapr Pub/Sub only).
- No stateful application logic; all mutable state persisted immediately.
- No refactoring of existing Phase 3/4 code unless critical bug fix.
- All new services must be independently deployable (separate Helm charts, container images, CI pipelines).
- Events must be immutable and include full context (no cross-reference lookups required by consumers).
- Secrets never logged, stored in code, or passed via environment variables (Dapr Secrets only).

## Governance

**Constitution Supersedes All Practices:** This constitution is the authoritative source for architectural and operational decisions. Code, PRs, and deployments must verify compliance with all principles.

**Amendment Process:**
1. Propose changes via issue or pull request with rationale.
2. Document impact on dependent artifacts (templates, runbooks, CI/CD workflows).
3. Require team consensus and explicit version bump.
4. Update dependent templates and documentation in same PR.

**Versioning:** Semantic versioning (MAJOR.MINOR.PATCH):
- **MAJOR:** Removal or redefinition of core principles (e.g., abandoning event-driven, switching to monolith).
- **MINOR:** New principle, new service category, or materially expanded guidance (e.g., adding Notification Service spec).
- **PATCH:** Clarifications, wording refinements, non-semantic corrections.

**Compliance Review:** Every 2 weeks during development; on every major release. PRs must reference constitution sections if they introduce new patterns or systems.

**Version**: 1.0.0 | **Ratified**: 2026-01-30 | **Last Amended**: 2026-01-30
