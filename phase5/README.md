# Todo Chatbot Event-Driven Microservices

This repository contains an event-driven microservices implementation of a Todo Chatbot application using Dapr and Apache Kafka for distributed communication.

## Architecture Overview

### Services
1. **Chat API**: Main Python/FastAPI service handling core business logic and event publishing
2. **Recurring Task Service**: Node.js service handling recurring task creation based on RRULE patterns
3. **Notification Service**: Node.js service managing task reminders and notifications
4. **Audit Service**: Node.js service maintaining immutable audit logs of all task changes

### Infrastructure Components
- **Apache Kafka**: Event streaming via Strimzi operator
- **Dapr**: Distributed application runtime for pub/sub, state management, and service invocation
- **Redis**: State store for reminders and other transient data
- **PostgreSQL**: Persistent storage for tasks and audit logs
- **Kubernetes**: Container orchestration platform

### Event Flow
1. Task CRUD operations in Chat API trigger events published to Kafka via Dapr
2. Recurring Task Service listens for TaskCompleted events and creates new occurrences
3. Notification Service schedules and delivers reminders based on due dates
4. Audit Service logs all task changes to maintain audit trail
5. Real-time updates broadcast to connected clients via WebSocket

## Features

### User Story 1 - Recurring Tasks
- Create tasks with recurrence rules (RRULE format)
- Automatically generates next occurrence when task is completed
- Supports various recurrence patterns (daily, weekly, monthly, etc.)

### User Story 2 - Due Dates and Reminders
- Assign due dates to tasks
- Set reminder offsets before due dates
- Automatic reminder notifications delivered to users

### User Story 6 - Audit Trail
- Immutable log of all task changes
- Track who made changes and when
- Support for querying audit history by task or date range

## Deployment

### Prerequisites
- Kubernetes cluster (Minikube, kind, or cloud provider)
- Helm 3.x
- Dapr installed in the cluster
- Strimzi Kafka operator deployed

### Installation
```bash
# Start infrastructure
minikube start
kubectl create namespace todo-app

# Install Kafka and Dapr components
kubectl apply -f helm/strimzi-kafka/
kubectl apply -f helm/dapr-components/

# Wait for infrastructure to be ready
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=kafka -n todo-app --timeout=300s

# Deploy the application
helm install todo-app helm/todo-chatbot/ --namespace todo-app
```

### Configuration
- Environment variables are managed via Helm values files
- Service-specific configurations are in their respective values files
- Infrastructure configurations are in the infrastructure Helm charts

## Operations

### Health Checks
Each service exposes a health check endpoint:
- Chat API: `GET /health`
- Recurring Task Service: `GET /health`
- Notification Service: `GET /health`
- Audit Service: `GET /health`

### Monitoring
- Dapr provides built-in metrics via Prometheus
- Structured logging with correlation IDs
- Distributed tracing with OpenTelemetry

### Scaling
- All services support horizontal scaling via Kubernetes Deployments
- Configure resource requests and limits in Helm values
- Use Horizontal Pod Autoscaler for automatic scaling

## Development

### Local Development
- Each service can be developed independently
- Services communicate via Dapr sidecars when deployed
- Local development can bypass Dapr for faster iteration

### Testing
- Unit tests for individual services
- Integration tests for event flows
- End-to-end tests for user stories

## Security

- mTLS encryption for all service-to-service communication
- Role-based access control (RBAC) for Kubernetes resources
- Secrets management via Kubernetes secrets
- Input validation at service boundaries
- Regular dependency vulnerability scanning

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License.