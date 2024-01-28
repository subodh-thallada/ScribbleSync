#!/bin/bash

# Build Docker Image
docker build -t my-application:v1 .

# Apply Kubernetes configurations
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

# Check the deployment status
kubectl rollout status deployment/my-application-deployment

# Scale the deployment
kubectl scale deployment my-application-deployment --replicas=3

# Update the deployment with a new image
kubectl set image deployment/my-application-deployment my-application=my-application:v2

# Check logs
# kubectl logs deployment/my-application-deployment

