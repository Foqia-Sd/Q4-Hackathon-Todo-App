# Phase 4 Quickstart Guide - Kubernetes Deployment

## Overview
This guide provides instructions for deploying the AI-powered Todo application using Kubernetes with Helm charts on a local Minikube cluster.

## Prerequisites
- Docker Desktop
- Minikube
- kubectl
- Helm v3
- kubectl-ai (optional, for AI-assisted operations)

## Setup Instructions

### 1. Start Minikube Cluster
```bash
minikube start
```

### 2. Build Docker Images
```bash
# Navigate to frontend directory and build image
cd frontend
docker build -t todo-frontend:latest .

# Navigate to backend directory and build image
cd ../backend
docker build -t todo-backend:fixed .
```

### 3. Load Images into Minikube
```bash
minikube image load todo-frontend:latest
minikube image load todo-backend:fixed
```

### 4. Deploy Using Helm
```bash
cd ../helm-chart
helm install todo-app .
```

### 5. Access the Application
```bash
# Get frontend URL
minikube service frontend --url

# Get backend URL
minikube service backend --url
```

## Helm Chart Configuration

### Values Override Example
```yaml
frontend:
  replicaCount: 1
  image:
    repository: todo-frontend
    tag: latest
  service:
    type: LoadBalancer
    port: 3000

backend:
  replicaCount: 1
  image:
    repository: todo-backend
    tag: fixed
  service:
    type: ClusterIP
    port: 8000
```

## Health Checks
Both frontend and backend deployments include:
- Liveness probes
- Readiness probes

## Scaling
Scale deployments using kubectl:
```bash
kubectl scale deployment/frontend --replicas=3
kubectl scale deployment/backend --replicas=2
```

## Cleanup
```bash
# Uninstall Helm release
helm uninstall todo-app

# Stop Minikube
minikube stop
```

## AI-Assisted Operations (Optional)

### Installing kubectl-ai
For AI-assisted Kubernetes operations, install the kubectl-ai plugin:

```bash
# Download and install kubectl-ai
curl -sL https://raw.githubusercontent.com/sozercan/kubectl-ai/main/install.sh | bash

# Or using go install (if Go is available)
go install github.com/sozercan/kubectl-ai@latest
```

### AI-Assisted Commands (When Available)
Once installed, you can use AI-assisted operations:

```bash
# Describe your deployed application with AI
kubectl ai "describe the todo-app deployment and its current status"

# Generate additional manifests
kubectl ai "generate a horizontal pod autoscaler for the frontend deployment"

# Troubleshoot issues
kubectl ai "analyze these logs and suggest fixes: $(kubectl logs <pod-name>)"

# Scale deployments with AI guidance
kubectl ai "scale the frontend deployment based on high traffic patterns"

# Get resource utilization insights
kubectl ai "show me resource usage of the todo-app and suggest optimizations"
```

### Troubleshooting

#### Common Issues
1. **Images not found**: Ensure images are loaded into Minikube using `minikube image load`
2. **Services not accessible**: Use `minikube service` command to get URLs
3. **Pods in CrashLoopBackOff**: Check logs with `kubectl logs <pod-name>`

### Useful Commands
```bash
# Check pod status
kubectl get pods

# Check service status
kubectl get services

# Check deployment status
kubectl get deployments

# View pod logs
kubectl logs <pod-name>

# Execute commands in pod
kubectl exec -it <pod-name> -- /bin/sh
```

## Architecture
- Frontend: Next.js application served via Nginx
- Backend: FastAPI application with SQLite database
- Communication: Frontend communicates with backend via REST API
- Deployment: Helm charts for consistent deployment
- Infrastructure: Kubernetes on Minikube (local)

## AI Integration
The backend includes an AI agent that can process natural language input for todo management using the Gemini API. If the API key is not available, the system falls back to a mock implementation.