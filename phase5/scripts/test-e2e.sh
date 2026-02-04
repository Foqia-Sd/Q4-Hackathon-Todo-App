#!/bin/bash
# Test script to verify end-to-end flow for Phase 5

echo "Starting end-to-end verification for Todo Chatbot Event-Driven Microservices..."

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "kubectl is not installed or not in PATH"
    exit 1
fi

# Check if helm is available
if ! command -v helm &> /dev/null; then
    echo "helm is not installed or not in PATH"
    exit 1
fi

echo "Checking if Kubernetes cluster is accessible..."
kubectl cluster-info

echo "Checking if Dapr is installed..."
kubectl get pods -n dapr-system

echo "Checking if Kafka is running..."
kubectl get pods -n todo-app | grep kafka

echo "Checking if all services are running..."
kubectl get pods -n todo-app

echo "Checking if all deployments are ready..."
kubectl get deployments -n todo-app

echo "Checking service statuses..."
kubectl get svc -n todo-app

echo "Checking if all Dapr components are configured..."
kubectl get components.dapr.io -n todo-app

echo "End-to-end verification completed."
echo ""
echo "To manually test the functionality:"
echo "1. Create a task with recurrence rule (US1)"
echo "2. Create a task with due date and reminder (US2)"
echo "3. Complete the recurring task and verify next occurrence is created"
echo "4. Wait for the reminder time and verify notification is sent"
echo "5. Check audit logs for all task operations (US6)"