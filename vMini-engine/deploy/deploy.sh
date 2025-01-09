#!/bin/bash

# Default to production for deployment
export ENVIRONMENT=${ENVIRONMENT:-production}

# Build the Docker image
docker build -t vmini-engine .

# Log in to Amazon ECR
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.us-west-2.amazonaws.com

# Tag and push the image
docker tag vmini-engine:latest $AWS_ACCOUNT_ID.dkr.ecr.us-west-2.amazonaws.com/vmini-engine:latest
docker push $AWS_ACCOUNT_ID.dkr.ecr.us-west-2.amazonaws.com/vmini-engine:latest

# Update the ECS service
aws ecs update-service --cluster vMini-engine-cluster --service vMini-engine-service --force-new-deployment 