#!/bin/bash

# Deployment script for using AWS access keys instead of IAM roles

echo "Deploying application with AWS access keys..."

# Step 1: Encode your AWS credentials
echo "Step 1: Encoding AWS credentials..."
python3 encode-aws-credentials.py

echo ""
echo "Step 2: Update the aws-secret.yaml file with the encoded values above"
echo "Step 3: Apply the AWS secret to your cluster"
echo ""

# Step 4: Apply the secret (uncomment after updating aws-secret.yaml)
# kubectl apply -f k8s/aws-secret.yaml

# Step 5: Apply the updated deployment
echo "Step 4: Applying the updated deployment..."
kubectl apply -f k8s/app/deployment.yaml

echo ""
echo "Deployment completed!"
echo "Check the logs to see if S3 download is working:"
echo "kubectl logs -f deployment/flask-app-deployment -n final" 