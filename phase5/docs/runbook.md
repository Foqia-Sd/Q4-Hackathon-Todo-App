# Operational Runbook - Todo Chatbot Event-Driven Microservices

## Overview
This runbook provides operational procedures for the event-driven microservices architecture of the Todo Chatbot application. This system implements a scalable, resilient event-driven architecture using Dapr and Apache Kafka for message brokering.

## System Architecture
- **Chat API**: Python/FastAPI service handling core business logic and event publishing
- **Recurring Task Service**: Node.js service for handling recurring tasks based on RRULE patterns
- **Notification Service**: Node.js service for task reminders and notifications with scheduling
- **Audit Service**: Node.js service for maintaining immutable audit logs of all task changes
- **Infrastructure**: Dapr for service mesh, Apache Kafka for messaging, PostgreSQL for persistence, Redis for state management

## Service Dependencies
- PostgreSQL database (for all services)
- Apache Kafka (for event streaming)
- Redis (for Dapr state management)
- Dapr runtime (for service mesh capabilities)
- Kubernetes cluster (for orchestration)

## Monitoring and Observability

### Health Checks
Each service exposes a health check endpoint:
- Chat API: `GET /health`
- Recurring Task Service: `GET /health`
- Notification Service: `GET /health`
- Audit Service: `GET /health`

### Metrics and Tracing
- Dapr provides built-in metrics via Prometheus endpoint (`/v1.0/metrics`)
- Distributed tracing using OpenTelemetry with Jaeger integration
- Service-to-service communication metrics
- Event processing latency metrics

### Logging
All services use structured logging:
- Chat API: JSON formatted logs with correlation IDs
- Node.js services: Winston logger with JSON format and structured metadata
- Log levels: INFO, WARN, ERROR, DEBUG
- All logs include timestamps, service names, and request IDs for correlation

## Common Operations

### 1. Starting the System
```bash
# Start infrastructure
minikube start
kubectl create namespace todo-app
kubectl apply -f helm/strimzi-kafka/
kubectl apply -f helm/dapr-components/

# Wait for Kafka and Dapr to be ready
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=kafka -n todo-app --timeout=300s
kubectl wait --for=condition=ready pod -l app=dapr-placement -n dapr-system --timeout=300s

# Deploy all services
helm install todo-app helm/todo-chatbot/ --namespace todo-app
```

### 2. Checking Service Status
```bash
kubectl get pods -n todo-app
kubectl get svc -n todo-app
kubectl get deployments -n todo-app
kubectl logs -f <pod-name> -n todo-app
kubectl describe pod <pod-name> -n todo-app
```

### 3. Scaling Services
```bash
kubectl scale deployment <deployment-name> --replicas=<count> -n todo-app
# Example: kubectl scale deployment todo-chat-api --replicas=3 -n todo-app
```

### 4. Configuration Management
```bash
# Update configuration without redeploying
kubectl edit configmap <configmap-name> -n todo-app
kubectl rollout restart deployment/<deployment-name> -n todo-app

# View current configuration
kubectl get configmaps -n todo-app
kubectl get secrets -n todo-app
```

### 5. Service Restart
```bash
# Restart a specific service
kubectl rollout restart deployment/<deployment-name> -n todo-app

# Restart all services
kubectl rollout restart deployment -n todo-app
```

## Troubleshooting

### Service Unavailable
1. Check pod status: `kubectl get pods -n todo-app`
2. Check logs: `kubectl logs <pod-name> -n todo-app`
3. Check events: `kubectl describe pod <pod-name> -n todo-app`
4. Verify dependencies (database connectivity, Kafka availability)
5. Check Dapr sidecar status: `kubectl logs <pod-name> -c daprd -n todo-app`

### Event Processing Issues
1. Check Kafka topics: `kubectl exec -it <kafka-pod> -- kafka-topics.sh --list --bootstrap-server localhost:9092`
2. Verify Dapr sidecars are running and healthy
3. Check event subscriptions in each service
4. Monitor consumer lag: `kubectl exec -it <kafka-pod> -- kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group <consumer-group>`
5. Check Dapr pubsub component status: `kubectl get components.dapr.io -n todo-app`

### Database Connectivity
1. Verify database pod is running: `kubectl get pods -n <db-namespace>`
2. Check connection strings in service configurations
3. Confirm network policies allow database access
4. Test connectivity: `kubectl run debug --image=postgres --rm -it -- psql -h <db-host> -U <db-user>`

### Dapr-Specific Issues
1. Check Dapr control plane: `kubectl get pods -n dapr-system`
2. Verify Dapr components: `kubectl get components.dapr.io -n todo-app`
3. Check Dapr placement service: `kubectl logs -l app=dapr-placement -n dapr-system`
4. Inspect Dapr sidecar logs: `kubectl logs <pod-name> -c daprd -n todo-app`

### Resource Constraints
1. Check resource usage: `kubectl top pods -n todo-app`
2. Check node capacity: `kubectl top nodes`
3. Review resource limits: `kubectl describe deployment <deployment-name> -n todo-app`
4. Check for evicted pods: `kubectl get pods -A --field-selector=status.phase=Failed`

## Maintenance Procedures

### 1. Routine Checks
- Monitor service health endpoints daily
- Review logs for errors/warnings
- Check database connection pools and performance
- Verify Kafka topic retention policies and partition distribution
- Monitor Dapr sidecar health and metrics
- Check resource utilization across all services

### 2. Backup Procedures
- PostgreSQL backup: `kubectl exec -it <postgres-pod> -- pg_dump -U <user> <database> > backup.sql`
- Backup Kafka topics if needed: `kubectl exec -it <kafka-pod> -- kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic <topic> --from-beginning > backup.json`
- Consider automated backup solutions for production using Velero for Kubernetes resources

### 3. Update Procedures
- Test updates in staging environment first
- Create backup before major updates
- Use rolling updates to minimize downtime: `kubectl set image deployment/<deployment-name> <container>=<new-image> -n todo-app`
- Monitor for issues post-deployment using health checks
- Have rollback plan ready: `kubectl rollout undo deployment/<deployment-name> -n todo-app`

### 4. Certificate and Secret Rotation
- Rotate database passwords regularly
- Update TLS certificates before expiration
- Refresh API keys and tokens periodically
- Use Kubernetes secrets rotation mechanisms

### 5. Log Rotation and Cleanup
- Configure log rotation to prevent disk space issues
- Archive old logs to external storage
- Clean up old Kafka topics that are no longer needed
- Remove old Kubernetes events and configmaps if needed

## Emergency Procedures

### Service Degradation
1. Isolate affected service by scaling down: `kubectl scale deployment <deployment-name> --replicas=0 -n todo-app`
2. Check resource utilization (CPU, Memory): `kubectl top pods -n todo-app`
3. Review recent changes or deployments: `kubectl rollout history deployment/<deployment-name> -n todo-app`
4. Scale up resources temporarily if needed: `kubectl patch deployment <deployment-name> -p '{"spec":{"template":{"spec":{"containers":[{"name":"<container-name>","resources":{"requests":{"cpu":"1000m","memory":"1Gi"},"limits":{"cpu":"2000m","memory":"2Gi"}}}]}}}}' -n todo-app`
5. Enable debug logging temporarily to gather more information

### Data Loss Prevention
1. Verify audit logs integrity by checking for gaps in sequence numbers
2. Restore from last known good backup immediately
3. Replay missed events from Kafka topic partitions
4. Validate data consistency across all services after restoration

### Complete System Outage
1. Assess scope of outage (single service, multiple services, infrastructure)
2. Activate backup systems if available
3. Follow disaster recovery procedures
4. Communicate with stakeholders about expected recovery time
5. Implement temporary workaround solutions if possible

### Security Incident
1. Isolate affected services immediately
2. Preserve evidence and logs for forensics
3. Notify security team
4. Assess scope of compromise
5. Implement security patches and updates
6. Conduct post-incident review

## Performance Tuning

### Database Optimization
- Index frequently queried fields (task ID, user ID, due date, status)
- Monitor slow query logs and optimize queries
- Optimize connection pooling (adjust min/max pool sizes based on load)
- Partition large tables by date ranges if needed
- Use read replicas for heavy read operations

### Event Processing
- Adjust Kafka partition counts based on concurrent consumers and load
- Monitor consumer lag across all topics
- Tune Dapr pub/sub settings (concurrency, retry policies)
- Configure appropriate message TTL and retention policies
- Optimize serialization formats (JSON vs Protobuf)

### Service Scaling
- Configure Horizontal Pod Autoscaler (HPA) based on CPU/memory metrics
- Set appropriate resource requests and limits
- Use Cluster Autoscaler for node-level scaling
- Implement circuit breaker patterns to prevent cascading failures
- Configure proper readiness/liveness probes

### Dapr Configuration
- Optimize Dapr sidecar configuration for performance
- Configure appropriate timeouts for service invocations
- Tune actor placement and rebalancing settings if using actors
- Optimize state store configuration (caching, connection pooling)

## Security Considerations
- Regular dependency vulnerability scanning using tools like Trivy or Snyk
- Secure secret management with Kubernetes secrets and sealed-secrets
- Network policies to restrict inter-service communication (only allow necessary connections)
- TLS encryption for all communications (in-transit and at-rest)
- Dapr security best practices: mTLS, service invocation scopes, component authentication
- Regular security audits of Dapr components and configurations
- Implement least-privilege RBAC for all services
- Monitor for security events and anomalies
- Regular security patching of underlying infrastructure
- Input validation and sanitization at all service boundaries

## Deployment Environments

### Development
- Local Minikube cluster
- Single-node Kafka setup
- In-memory databases for testing
- Debug logging enabled

### Staging
- Dedicated Kubernetes cluster
- Production-like Kafka configuration
- Separate database from production
- Standard logging and monitoring

### Production
- Multi-node Kubernetes cluster with high availability
- Multi-node Kafka cluster with replication
- Production database with backups
- Optimized resource allocation
- Comprehensive monitoring and alerting

## Conclusion

This runbook provides the essential operational procedures for maintaining the Todo Chatbot event-driven microservices system. Regular updates to this document should be made as the system evolves, and operators should practice emergency procedures in non-production environments.

For additional support:
- Check the service logs in the Kubernetes dashboard
- Consult the individual service README files in their respective directories
- Refer to the Dapr documentation for platform-specific issues
- Contact the development team through the established communication channels