#!/bin/bash

# Register new task definition
TASK_DEF_ARN=$(aws ecs register-task-definition \
    --cli-input-json file://deploy/aws/task-definition.json \
    --query 'taskDefinition.taskDefinitionArn' \
    --output text)

echo "Registered new task definition: $TASK_DEF_ARN"

# Update the service with the new task definition and network configuration
aws ecs update-service \
    --cluster vMini-engine-production \
    --service vmini-engine-service-production \
    --task-definition "$TASK_DEF_ARN" \
    --network-configuration '{
        "awsvpcConfiguration": {
            "subnets": ["subnet-08e2f4a63424670d9"],
            "securityGroups": ["sg-04515fc78b0af01dd"],
            "assignPublicIp": "ENABLED"
        }
    }' \
    --force-new-deployment

echo "Service update initiated. Monitoring deployment..."

# Monitor deployment
aws ecs describe-services \
    --cluster vMini-engine-production \
    --services vmini-engine-service-production \
    --query 'services[0].{Status:status,DesiredCount:desiredCount,RunningCount:runningCount,Events:events[0].message}' \
    --output table 