#!/bin/bash

# Default to production for deployment
export ENVIRONMENT=${ENVIRONMENT:-production}
export AWS_ACCOUNT_ID=047719630676
export AWS_REGION=us-west-2

# Set up buildx for multi-platform builds
docker buildx create --use --name vMini-builder || true

# Build and push directly to ECR
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

# Build and push the image directly
IMAGE_URI="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/vmini-engine-production:latest"
docker buildx build \
    --platform linux/amd64 \
    --tag $IMAGE_URI \
    --push \
    .

# Get the exact image digest
IMAGE_DIGEST=$(aws ecr describe-images \
    --repository-name vmini-engine-production \
    --image-ids imageTag=latest \
    --query 'imageDetails[0].imageDigest' \
    --output text)

# Update task definition with exact image reference
sed -i.bak "s|\"image\": \".*\"|\"image\": \"$IMAGE_URI@$IMAGE_DIGEST\"|" deploy/aws/task-definition.json

# Register the new task definition
TASK_DEFINITION_ARN=$(aws ecs register-task-definition \
    --cli-input-json file://deploy/aws/task-definition.json \
    --query 'taskDefinition.taskDefinitionArn' \
    --output text)

echo "Registered new task definition: $TASK_DEFINITION_ARN"

# Update the ECS service with the new task definition and network configuration
aws ecs update-service \
    --cluster vMini-engine-production \
    --service vmini-engine-service-production \
    --task-definition "$TASK_DEFINITION_ARN" \
    --network-configuration '{
        "awsvpcConfiguration": {
            "subnets": ["subnet-08e2f4a63424670d9"],
            "securityGroups": ["sg-04515fc78b0af01dd"],
            "assignPublicIp": "ENABLED"
        }
    }' \
    --force-new-deployment

# Monitor deployment status
echo "Monitoring deployment status..."
aws ecs describe-services \
    --cluster vMini-engine-production \
    --services vmini-engine-service-production \
    --query 'services[0].{Status:status,Desired:desiredCount,Running:runningCount,Events:events[0:3].message}' \
    --output table

# Check task status and get reason for any stopped tasks
echo "Checking task status..."
TASK_ARN=$(aws ecs list-tasks \
    --cluster vMini-engine-production \
    --service-name vmini-engine-service-production \
    --query 'taskArns[0]' \
    --output text)

if [ ! -z "$TASK_ARN" ]; then
    aws ecs describe-tasks \
        --cluster vMini-engine-production \
        --tasks "$TASK_ARN" \
        --query 'tasks[].{LastStatus:lastStatus,StoppedReason:stoppedReason,Containers:containers[].{Name:name,Reason:reason}}' \
        --output table
else
    echo "No tasks found running"
fi 