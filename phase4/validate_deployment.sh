#!/bin/bash

echo "=== AI-Powered Todo App - Deployment Validation ==="

echo "1. Checking Kubernetes cluster status..."
kubectl cluster-info

echo ""
echo "2. Checking pods status..."
kubectl get pods

echo ""
echo "3. Checking services status..."
kubectl get services

echo ""
echo "4. Checking deployments status..."
kubectl get deployments

echo ""
echo "5. Checking Helm release status..."
helm status todo-app

echo ""
echo "6. Testing backend API connectivity..."

# Get backend service URL
BACKEND_URL=$(minikube service backend --url 2>/dev/null || echo "http://127.0.0.1:51402")

# Test API root endpoint
echo "Testing backend API at ${BACKEND_URL}"
curl -s -o /dev/null -w "Status Code: %{http_code}\n" "${BACKEND_URL}/"

echo ""
echo "7. Testing frontend availability..."

# Get frontend service URL
FRONTEND_URL=$(minikube service frontend --url 2>/dev/null || echo "http://127.0.0.1:51310")

# Test frontend
echo "Testing frontend at ${FRONTEND_URL}"
curl -s -o /dev/null -w "Status Code: %{http_code}\n" "${FRONTEND_URL}/"

echo ""
echo "8. Summary of Helm chart features:"
echo "- Frontend and backend deployments with health checks"
echo "- LoadBalancer and ClusterIP services"
echo "- Configurable resource limits and requests"
echo "- Ingress support (disabled by default)"
echo "- Easy scaling and upgrades"

echo ""
echo "Validation completed!"