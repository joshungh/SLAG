#!/bin/bash

# Get the Redis cluster security group
REDIS_SG=$(aws cloudformation describe-stacks \
    --stack-name vmini-engine-redis \
    --query 'Stacks[0].Outputs[?OutputKey==`RedisSecurityGroupId`].OutputValue' \
    --output text)

if [ -z "$REDIS_SG" ]; then
    echo "Error: Could not get Redis security group ID"
    exit 1
fi

echo "Redis Security Group: $REDIS_SG"

# Get the ECS service security group - adjust stack name if needed
ECS_STACK_NAME="vmini-engine-production"  # or whatever your ECS stack is named
ECS_SG=$(aws cloudformation describe-stacks \
    --stack-name $ECS_STACK_NAME \
    --query 'Stacks[0].Outputs[?contains(OutputKey,`ServiceSecurityGroup`)].OutputValue' \
    --output text)

if [ -z "$ECS_SG" ]; then
    echo "Error: Could not get ECS security group ID"
    exit 1
fi

echo "ECS Security Group: $ECS_SG"

echo "Updating Redis security group rules..."

# Remove existing rules first
aws ec2 revoke-security-group-ingress \
    --group-id $REDIS_SG \
    --protocol tcp \
    --port 6379 \
    --source-group $ECS_SG || true

# Add new rule
aws ec2 authorize-security-group-ingress \
    --group-id $REDIS_SG \
    --protocol tcp \
    --port 6379 \
    --source-group $ECS_SG \
    --description "Allow access from vMini-engine ECS service"

echo "Security group update complete!" 