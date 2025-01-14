#!/bin/bash

# Set variables
ENVIRONMENT="production"
AWS_REGION="us-west-2"
VPC_ID="vpc-084087a335373ed6c"
SUBNET_1="subnet-08e2f4a63424670d9"
SUBNET_2="subnet-07754accd2f3042f7"
STACK_PREFIX="vMini-engine"

# Function to wait for stack completion
wait_for_stack() {
    local stack_name=$1
    echo "Waiting for stack $stack_name..."
    aws cloudformation wait stack-update-complete --stack-name $stack_name
}

# Deploy ECS Service Stack
echo "Deploying ECS service stack..."
aws cloudformation create-stack \
    --stack-name "${STACK_PREFIX}-ecs-service" \
    --template-body file://ecs-service.yml \
    --parameters \
        ParameterKey=Environment,ParameterValue=$ENVIRONMENT \
        ParameterKey=VpcId,ParameterValue=$VPC_ID \
        ParameterKey=PublicSubnet1,ParameterValue=$SUBNET_1 \
        ParameterKey=PublicSubnet2,ParameterValue=$SUBNET_2 \
    --capabilities CAPABILITY_NAMED_IAM

wait_for_stack "${STACK_PREFIX}-ecs-service"

echo "Service deployment complete!" 