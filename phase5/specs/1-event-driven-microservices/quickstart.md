# Quickstart: Phase 5 Local Development

**Feature**: 1-event-driven-microservices
**Date**: 2026-01-30

## Prerequisites

- Docker Desktop or Rancher Desktop
- Minikube 1.30+
- kubectl configured
- Helm 3.x
- Dapr CLI 1.12+
- Node.js 20 LTS
- Git

## Quick Setup (TL;DR)

```bash
# 1. Start Minikube
minikube start --cpus=4 --memory=8192 --driver=docker

# 2. Install Dapr
dapr init -k --wait

# 3. Deploy infrastructure (Kafka + Redis)
./scripts/setup-infra.sh

# 4. Deploy application
helm install todo-chatbot ./helm/todo-chatbot -f ./helm/todo-chatbot/values-minikube.yaml

# 5. Access the app
minikube service chat-api --url
```

---

## Detailed Setup

### Step 1: Start Minikube

```bash
# Start with sufficient resources for Kafka and all services
minikube start \
  --cpus=4 \
  --memory=8192 \
  --disk-size=20g \
  --driver=docker

# Enable required addons
minikube addons enable ingress
minikube addons enable metrics-server

# Verify cluster is ready
kubectl get nodes
```

### Step 2: Install Dapr

```bash
# Initialize Dapr on Kubernetes
dapr init -k --wait

# Verify Dapr is running
dapr status -k

# Expected output:
#   NAME                   NAMESPACE    HEALTHY  STATUS   VERSION
#   dapr-sidecar-injector  dapr-system  True     Running  1.12.x
#   dapr-operator          dapr-system  True     Running  1.12.x
#   dapr-placement-server  dapr-system  True     Running  1.12.x
#   dapr-sentry            dapr-system  True     Running  1.12.x
```

### Step 3: Install Strimzi Kafka Operator

```bash
# Add Strimzi Helm repo
helm repo add strimzi https://strimzi.io/charts/
helm repo update

# Install operator
helm install strimzi-kafka-operator strimzi/strimzi-kafka-operator \
  --namespace kafka \
  --create-namespace \
  --wait

# Deploy Kafka cluster
kubectl apply -f ./helm/strimzi-kafka/templates/kafka-cluster.yaml -n kafka

# Wait for Kafka to be ready (takes 2-3 minutes)
kubectl wait kafka/kafka-cluster --for=condition=Ready --timeout=300s -n kafka

# Create topics
kubectl apply -f ./helm/strimzi-kafka/templates/kafka-topics.yaml -n kafka
```

### Step 4: Install Redis

```bash
# Add Bitnami repo
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

# Install Redis (no auth for local dev)
helm install redis bitnami/redis \
  --namespace todo \
  --create-namespace \
  --set auth.enabled=false \
  --set replica.replicaCount=0 \
  --wait
```

### Step 5: Deploy Dapr Components

```bash
# Apply Dapr component definitions
kubectl apply -f ./helm/dapr-components/templates/ -n todo
```

### Step 6: Deploy Application

```bash
# Deploy all services
helm install todo-chatbot ./helm/todo-chatbot \
  -f ./helm/todo-chatbot/values-minikube.yaml \
  -n todo \
  --wait

# Verify all pods are running
kubectl get pods -n todo -l app.kubernetes.io/part-of=todo-chatbot
```

---

## Accessing Services

### Chat API (Main Application)

```bash
# Get service URL
minikube service chat-api -n todo --url

# Or use port-forward
kubectl port-forward svc/chat-api 3000:3000 -n todo
# Access at http://localhost:3000
```

### Dapr Dashboard

```bash
# Open Dapr dashboard
dapr dashboard -k

# Access at http://localhost:8080
```

### Audit Service API

```bash
kubectl port-forward svc/audit-service 3003:3000 -n todo
# Access at http://localhost:3003/audit/entries
```

---

## Local Development Workflow

### Running Services Locally with Dapr

For faster iteration, run services locally while connected to Minikube infrastructure:

```bash
# Terminal 1: Run Chat API with Dapr sidecar
cd services/chat-api
dapr run --app-id chat-api --app-port 3000 --dapr-http-port 3500 -- npm run dev

# Terminal 2: Run RecurringTaskService
cd services/recurring-task-service
dapr run --app-id recurring-task-service --app-port 3001 --dapr-http-port 3501 -- npm run dev

# Terminal 3: Run NotificationService
cd services/notification-service
dapr run --app-id notification-service --app-port 3002 --dapr-http-port 3502 -- npm run dev

# Terminal 4: Run AuditService
cd services/audit-service
dapr run --app-id audit-service --app-port 3003 --dapr-http-port 3503 -- npm run dev
```

### Port-Forward Kafka for Local Development

```bash
# Forward Kafka broker
kubectl port-forward svc/kafka-cluster-kafka-bootstrap 9092:9092 -n kafka

# Forward Redis
kubectl port-forward svc/redis-master 6379:6379 -n todo
```

### Viewing Logs

```bash
# All pods
kubectl logs -l app.kubernetes.io/part-of=todo-chatbot -n todo --tail=100 -f

# Specific service
kubectl logs -l app=recurring-task-service -n todo -f

# Dapr sidecar logs
kubectl logs -l app=chat-api -n todo -c daprd -f
```

---

## Testing the Event Flow

### 1. Create a Task with Recurrence

```bash
curl -X POST http://localhost:3000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Weekly standup",
    "description": "Team sync meeting",
    "dueDate": "2026-02-03T09:00:00Z",
    "priority": "HIGH",
    "tags": ["meetings", "team"],
    "recurrenceRule": "FREQ=WEEKLY;BYDAY=MO"
  }'
```

### 2. Complete the Task (Triggers Recurrence)

```bash
curl -X PATCH http://localhost:3000/api/tasks/{taskId} \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'
```

### 3. Verify Next Occurrence Created

```bash
# Check for new task
curl http://localhost:3000/api/tasks

# Check audit log
curl http://localhost:3003/audit/entries?action=CREATED
```

### 4. Check Reminder Scheduling

```bash
# View reminder state in Redis
kubectl exec -it redis-master-0 -n todo -- redis-cli KEYS "reminder:*"
```

---

## Troubleshooting

### Dapr Sidecar Not Injecting

```bash
# Check namespace has Dapr annotation
kubectl get namespace todo -o yaml | grep dapr

# Add if missing
kubectl label namespace todo dapr.io/inject=true
```

### Kafka Connection Issues

```bash
# Check Kafka pods
kubectl get pods -n kafka

# Check Kafka logs
kubectl logs kafka-cluster-kafka-0 -n kafka

# Test Kafka connectivity
kubectl run kafka-test --rm -it --image=bitnami/kafka -- \
  kafka-console-producer.sh --broker-list kafka-cluster-kafka-bootstrap.kafka:9092 --topic test
```

### Service Not Receiving Events

```bash
# Check Dapr subscriptions
kubectl get subscriptions.dapr.io -n todo

# Check service logs for subscription registration
kubectl logs -l app=recurring-task-service -n todo | grep subscription
```

### Redis State Store Issues

```bash
# Check Redis connectivity
kubectl exec -it redis-master-0 -n todo -- redis-cli PING

# View all keys
kubectl exec -it redis-master-0 -n todo -- redis-cli KEYS "*"
```

---

## Cleanup

```bash
# Uninstall application
helm uninstall todo-chatbot -n todo

# Uninstall Redis
helm uninstall redis -n todo

# Delete Kafka cluster
kubectl delete kafka kafka-cluster -n kafka

# Uninstall Strimzi operator
helm uninstall strimzi-kafka-operator -n kafka

# Uninstall Dapr
dapr uninstall -k

# Stop Minikube
minikube stop

# Delete cluster (optional)
minikube delete
```

---

## Next Steps

1. Review [plan.md](./plan.md) for implementation sequence
2. Review [data-model.md](./data-model.md) for entity schemas
3. Review `contracts/` for event schemas
4. Run `/sp.tasks` to generate implementation tasks
