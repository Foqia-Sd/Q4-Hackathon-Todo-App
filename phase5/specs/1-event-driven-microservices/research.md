# Phase 0 Research: Event-Driven Microservices

**Feature**: 1-event-driven-microservices
**Date**: 2026-01-30
**Status**: Complete

## Research Summary

This document captures technology decisions and patterns researched for Phase 5 implementation.

---

## 1. Dapr Pub/Sub with Kafka

### Decision
Use Dapr Pub/Sub component with Kafka backend for all event-driven communication.

### Rationale
- **Abstraction**: Application code uses Dapr SDK; no Kafka client libraries needed
- **Portability**: Switch from Strimzi to managed Kafka (Confluent, Redpanda) by changing Dapr component config only
- **Built-in features**: Retries, dead-letter topics, CloudEvents support, tracing
- **Constitution compliance**: Principle III mandates Dapr-first external access

### Alternatives Considered
| Alternative | Rejected Because |
|-------------|-----------------|
| Direct KafkaJS client | Violates constitution; couples code to Kafka implementation |
| RabbitMQ | Less cloud-native; Kafka better for event sourcing patterns |
| Redis Streams | Less mature for pub/sub; Kafka has better durability guarantees |

### Implementation Pattern
```typescript
// Publisher (Chat API)
import { DaprClient } from "@dapr/dapr";

const daprClient = new DaprClient();
await daprClient.pubsub.publish("task-pubsub", "task-events", {
  specversion: "1.0",
  type: "com.todo.task.created",
  source: "/services/chat-api",
  data: { taskId, task, action: "CREATED" }
});

// Subscriber (RecurringTaskService)
app.post("/task-events", async (req, res) => {
  const event = req.body;
  if (event.type === "com.todo.task.completed") {
    await handleTaskCompleted(event.data);
  }
  res.sendStatus(200);
});
```

### Configuration
```yaml
# Dapr subscription
apiVersion: dapr.io/v2alpha1
kind: Subscription
metadata:
  name: recurring-task-sub
spec:
  pubsubname: task-pubsub
  topic: task-events
  routes:
    default: /task-events
  scopes:
    - recurring-task-service
```

---

## 2. Strimzi Kafka Operator

### Decision
Use Strimzi Kafka Operator for local Minikube Kafka deployment.

### Rationale
- **Kubernetes-native**: CRD-based configuration; GitOps friendly
- **Production parity**: Same patterns work in production clusters
- **Resource efficiency**: Lightweight single-broker config for local dev
- **Topic management**: Declarative KafkaTopic CRDs

### Alternatives Considered
| Alternative | Rejected Because |
|-------------|-----------------|
| Docker Compose Kafka | Not Kubernetes-native; different deployment model |
| Confluent Operator | Heavier footprint; commercial features not needed |
| Bitnami Kafka Helm | Less feature-rich; no CRD-based topic management |

### Minikube Configuration
```yaml
# Minimal Kafka cluster for local development
apiVersion: kafka.strimzi.io/v1beta2
kind: Kafka
metadata:
  name: kafka-cluster
spec:
  kafka:
    version: 3.6.0
    replicas: 1
    listeners:
      - name: plain
        port: 9092
        type: internal
        tls: false
    storage:
      type: ephemeral
    resources:
      requests:
        memory: 512Mi
        cpu: 250m
      limits:
        memory: 1Gi
        cpu: 500m
  zookeeper:
    replicas: 1
    storage:
      type: ephemeral
    resources:
      requests:
        memory: 256Mi
        cpu: 100m
```

### Topic Definitions
```yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaTopic
metadata:
  name: task-events
  labels:
    strimzi.io/cluster: kafka-cluster
spec:
  partitions: 3
  replicas: 1
  config:
    retention.ms: 604800000  # 7 days
---
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaTopic
metadata:
  name: task-reminders
  labels:
    strimzi.io/cluster: kafka-cluster
spec:
  partitions: 1
  replicas: 1
---
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaTopic
metadata:
  name: task-updates
  labels:
    strimzi.io/cluster: kafka-cluster
spec:
  partitions: 3
  replicas: 1
```

---

## 3. iCalendar RRULE for Recurrence

### Decision
Use `rrule` npm package for iCalendar RFC 5545 recurrence rule parsing.

### Rationale
- **Standard compliance**: Full RFC 5545 RRULE support
- **Interoperability**: Same format used by Google Calendar, Outlook, etc.
- **Edge case handling**: Handles month-end dates, leap years, timezone issues
- **TypeScript support**: Has type definitions

### Alternatives Considered
| Alternative | Rejected Because |
|-------------|-----------------|
| Custom implementation | Error-prone; doesn't handle edge cases |
| cron expressions | Less expressive for "every 2nd Tuesday" patterns |
| later.js | Less maintained; fewer features |

### Implementation Pattern
```typescript
import { RRule, RRuleSet } from 'rrule';

function getNextOccurrence(rruleString: string, afterDate: Date): Date | null {
  const rule = RRule.fromString(rruleString);
  const next = rule.after(afterDate, true);
  return next;
}

// Example RRULE strings:
// Daily: "FREQ=DAILY"
// Every Monday: "FREQ=WEEKLY;BYDAY=MO"
// Monthly on 15th: "FREQ=MONTHLY;BYMONTHDAY=15"
// Last day of month: "FREQ=MONTHLY;BYMONTHDAY=-1"
```

### Edge Cases Handled
| Case | RRULE Behavior |
|------|----------------|
| Feb 30 (invalid date) | Skips to next valid occurrence |
| Leap year Feb 29 | Handled correctly; skipped in non-leap years |
| Timezone changes (DST) | Use UTC internally; convert for display |
| End of recurrence | UNTIL or COUNT parameters respected |

---

## 4. Dapr Cron Bindings

### Decision
Use Dapr Cron Input Binding for scheduled reminder checks.

### Rationale
- **Dapr-native**: No external cron job manager needed
- **Per-service triggers**: Each service can have its own cron schedule
- **Reliable**: Dapr handles missed triggers on service restart
- **Constitution compliance**: Principle III prohibits K8s CronJobs

### Alternatives Considered
| Alternative | Rejected Because |
|-------------|-----------------|
| Kubernetes CronJob | Constitution prohibits; separate pod overhead |
| node-cron in-process | Stateful; doesn't survive pod restarts |
| External scheduler (Airflow) | Over-engineered for simple periodic checks |

### Configuration
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
scopes:
  - notification-service
```

### Handler Pattern
```typescript
// notification-service/src/handlers/cron-trigger.handler.ts
app.post("/check-reminders", async (req, res) => {
  const now = new Date();
  const pendingReminders = await daprClient.state.query("statestore", {
    filter: {
      AND: [
        { EQ: { "value.status": "PENDING" } },
        { LTE: { "value.triggerTime": now.toISOString() } }
      ]
    }
  });

  for (const reminder of pendingReminders.results) {
    await sendReminder(reminder.data);
    await markReminderSent(reminder.key);
  }

  res.sendStatus(200);
});
```

---

## 5. Event Schema Versioning

### Decision
Use CloudEvents v1.0 format with semantic versioning for event types.

### Rationale
- **Industry standard**: CNCF CloudEvents specification
- **Dapr native**: Dapr Pub/Sub uses CloudEvents by default
- **Extensibility**: Custom attributes without breaking consumers
- **Observability**: Standard fields for tracing and correlation

### Alternatives Considered
| Alternative | Rejected Because |
|-------------|-----------------|
| Custom JSON format | No tooling support; reinventing the wheel |
| Protobuf | Over-engineered for this scale; reduces debuggability |
| Avro with Schema Registry | Additional infrastructure; overkill for 3 services |

### Event Type Naming Convention
```
com.todo.task.<action>
com.todo.task.created
com.todo.task.updated
com.todo.task.completed
com.todo.task.deleted
```

### Versioning Strategy
- **Backward compatible changes**: Add new optional fields; no version bump
- **Breaking changes**: New event type (e.g., `com.todo.task.v2.created`)
- **Consumer resilience**: Ignore unknown fields; use sensible defaults

### Event Schema (JSON Schema)
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://todo.example.com/schemas/task-event.json",
  "type": "object",
  "required": ["specversion", "type", "source", "id", "time", "data"],
  "properties": {
    "specversion": { "const": "1.0" },
    "type": {
      "type": "string",
      "pattern": "^com\\.todo\\.task\\.(created|updated|completed|deleted)$"
    },
    "source": { "type": "string", "format": "uri-reference" },
    "id": { "type": "string", "format": "uuid" },
    "time": { "type": "string", "format": "date-time" },
    "datacontenttype": { "const": "application/json" },
    "data": {
      "type": "object",
      "required": ["taskId", "userId", "action", "task"],
      "properties": {
        "taskId": { "type": "string", "format": "uuid" },
        "userId": { "type": "string", "format": "uuid" },
        "action": { "enum": ["CREATED", "UPDATED", "COMPLETED", "DELETED"] },
        "task": { "$ref": "#/$defs/task" },
        "changes": { "type": "object" },
        "correlationId": { "type": "string", "format": "uuid" }
      }
    }
  },
  "$defs": {
    "task": {
      "type": "object",
      "properties": {
        "id": { "type": "string", "format": "uuid" },
        "title": { "type": "string" },
        "description": { "type": "string" },
        "completed": { "type": "boolean" },
        "dueDate": { "type": "string", "format": "date-time" },
        "priority": { "enum": ["HIGH", "MEDIUM", "LOW", "NONE"] },
        "tags": { "type": "array", "items": { "type": "string" } },
        "recurrenceRule": { "type": "string" }
      }
    }
  }
}
```

---

## 6. State Store Strategy

### Decision
Use Redis-backed Dapr State Store for service-specific ephemeral state.

### Rationale
- **Fast reads/writes**: Sub-millisecond latency for reminder lookups
- **TTL support**: Auto-expire stale state entries
- **Query support**: Dapr state query API for filtering reminders
- **Separation of concerns**: Domain data in PostgreSQL; service state in Redis

### State Partitioning
| Service | State Store | Data |
|---------|-------------|------|
| RecurringTaskService | Redis | Last processed event per task (idempotency) |
| NotificationService | Redis | Scheduled reminders (pending, sent status) |
| AuditService | PostgreSQL | Audit entries (permanent, queryable) |

### State Key Design
```
// Idempotency keys (RecurringTaskService)
recurring:processed:{eventId}

// Reminder state (NotificationService)
reminder:{reminderId}
reminder:task:{taskId}  // Index for lookup by task
```

---

## Resolved Clarifications

All technical unknowns from the plan have been resolved:

| Unknown | Resolution |
|---------|------------|
| Event format | CloudEvents v1.0 |
| Recurrence library | rrule.js |
| Local Kafka | Strimzi Operator |
| Cron mechanism | Dapr Cron Binding |
| Schema versioning | Event type naming + ignore unknown fields |
| State store | Redis via Dapr; PostgreSQL for audit |

---

## References

- [Dapr Pub/Sub Documentation](https://docs.dapr.io/developing-applications/building-blocks/pubsub/)
- [Strimzi Quickstart](https://strimzi.io/quickstarts/)
- [rrule.js GitHub](https://github.com/jakubroztocil/rrule)
- [CloudEvents Specification](https://cloudevents.io/)
- [Dapr Bindings](https://docs.dapr.io/developing-applications/building-blocks/bindings/)
