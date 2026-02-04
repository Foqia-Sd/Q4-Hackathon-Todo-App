---
id: 001
title: Phase 5 Constitution
stage: constitution
date: 2026-01-30
surface: agent
model: claude-haiku-4-5-20251001
feature: none
branch: main
user: user
command: /sp.constitution
labels: ["architecture", "event-driven", "microservices", "dapr", "kubernetes"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - none
---

## Prompt

Create a constitution for Phase 5 of an AI-powered Todo Chatbot.

Goals:
- Extend Phase 4 Kubernetes app with advanced todo features and event-driven architecture.
- Keep all existing CRUD and AI chat functionality unchanged.
- Use microservices and loose coupling.

Mandatory rules:
- No refactoring of existing Phase 3/4 business logic.
- New capabilities must be added as separate services.
- Communication between services must be event-driven using Kafka via Dapr Pub/Sub.
- All external systems (Kafka, DB, secrets) must be accessed through Dapr sidecar, not direct clients.
- System must run first on Minikube, then unchanged on cloud Kubernetes (Oracle Cloud).
- Deployment must be containerized and managed with Helm charts.
- CI/CD must be implemented using GitHub Actions.

Architecture principles:
- Chat API publishes task events.
- Specialized services consume events:
  - Recurring Task Service
  - Notification Service
  - Audit/Activity Service
- Use Dapr building blocks: Pub/Sub, State, Bindings (cron), Service Invocation, Secrets.
- Stateless services; persistence via database or Dapr state store.

Success criteria:
- Recurring tasks auto-create next occurrence.
- Due-date reminders are triggered asynchronously.
- All task changes emit events and are logged.
- Helm charts deploy on Minikube and cloud without code changes.

## Response snapshot

Created Phase 5 Constitution (v1.0.0) with 7 core principles:

1. **Preserve Existing Functionality** – No refactoring of Phase 3/4 code; all new features as separate services.
2. **Event-Driven Microservices Architecture** – Services communicate via Dapr Pub/Sub + Kafka; loosely coupled, stateless.
3. **Dapr-First External Access** – All external systems (Kafka, DB, secrets, cron) routed through Dapr sidecars.
4. **Infrastructure as Code & Helm Deployment** – All deployments via parameterized Helm charts (environment-agnostic).
5. **CI/CD via GitHub Actions** – Automated builds, tests, image pushes, and deployments on every commit.
6. **Stateless Services & Persistent State via Dapr State Store or Database** – No in-memory or filesystem state; horizontal scaling enabled.
7. **Domain-Driven Event Publishing** – Chat API is authoritative event publisher; services react without feedback loops.

Additional sections cover:
- Three specialized event consumers (Recurring Task, Notification, Audit/Activity services).
- External System Access Rules (Kafka, Database, Secrets, Cron, Service-to-Service).
- Deployment & Environment Portability (Helm chart structure, values-minikube.yaml and values-oracle-cloud.yaml).
- Success Criteria & Acceptance Tests (5 measurable acceptance criteria).
- Constraints & Non-Negotiables (6 architectural guardrails).
- Governance (Amendment process, Versioning, Compliance review cadence).

File written to: `.specify/memory/constitution.md` (118 lines).

## Outcome

- ✅ **Impact:** Establishes authoritative governance framework for Phase 5; enables event-driven microservices architecture with Dapr and Kubernetes portability.
- 🧪 **Tests:** Constitution defines 5 measurable success criteria (recurrence latency, reminder delivery, audit completeness, Helm portability, CI/CD automation).
- 📁 **Files:** `.specify/memory/constitution.md` (new, 118 lines).
- 🔁 **Next prompts:** Create feature specs for Recurring Task Service, Notification Service, Audit Service; Design Dapr components; Build CI/CD workflow templates; Create Helm chart scaffolds.
- 🧠 **Reflection:** Constitution balances prescriptive architecture (event-driven, Dapr-first) with enough flexibility for implementation choices. Emphasis on environment portability (Minikube → Oracle Cloud) and zero breaking changes supports low-risk rollout.

## Evaluation notes (flywheel)

- **Failure modes observed:** None; constitution is prescriptive baseline.
- **Graders run and results (PASS/FAIL):** Not applicable (governance document, not executable).
- **Prompt variant (if applicable):** None.
- **Next experiment:** Validate constitution against existing Phase 4 codebase structure to identify any conflicts or gaps; create ADRs for event schema versioning and service discovery patterns.
