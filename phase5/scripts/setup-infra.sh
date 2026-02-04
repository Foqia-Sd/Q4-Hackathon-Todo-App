#!/bin/bash
set -e

# Setup Infrastructure Script for Todo Chatbot Phase 5
# Installs prerequisites (Strimzi, Dapr, Redis) on Minikube

echo "🚀 Starting Infrastructure Setup..."

# Check prerequisites
if ! command -v helm &> /dev/null; then
    echo "❌ Helm is not installed. Please install Helm 3.x"
    exit 1
fi

if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl is not installed. Please install kubectl"
    exit 1
fi

# 1. Install Dapr
echo "📦 Installing Dapr..."
dapr init -k --wait
echo "✅ Dapr installed."

# 2. Install Strimzi Kafka Operator
echo "📦 Installing Strimzi Kafka Operator..."
helm repo add strimzi https://strimzi.io/charts/
helm repo update
helm upgrade --install strimzi-kafka-operator strimzi/strimzi-kafka-operator \
  --namespace default \
  --wait
echo "✅ Strimzi Operator installed."

# 3. Deploy Kafka Cluster & Topics
echo "📦 Deploying Kafka Cluster..."
helm upgrade --install kafka ./helm/strimzi-kafka --wait
echo "✅ Kafka Cluster deployed."

# 4. Install Redis (for Dapr State Store)
echo "📦 Installing Redis..."
helm repo add bitnami https://charts.bitnami.com/bitnami
helm upgrade --install redis bitnami/redis \
  --set auth.enabled=true \
  --set auth.password=redis-password \
  --wait
echo "✅ Redis installed."

# 5. Deploy Dapr Components
echo "📦 Deploying Dapr Components..."
helm upgrade --install dapr-config ./helm/dapr-components --wait
echo "✅ Dapr Components deployed."

echo "🎉 Infrastructure setup complete!"
echo "Kafka Bootstrap: kafka-cluster-kafka-bootstrap:9092"
echo "Redis Host: redis-master:6379"
