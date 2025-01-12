#!/bin/bash

# Set variables
ENVIRONMENT="production"
AWS_REGION="us-west-2"
VPC_ID="vpc-084087a335373ed6c"
STACK_PREFIX="vMini-engine"

# Function to wait for stack completion
wait_for_stack() {
    local stack_name=$1
    echo "Waiting for stack $stack_name..."
    aws cloudformation wait stack-create-complete --stack-name $stack_name
}

# Deploy Security Stack
echo "Deploying security stack..."
aws cloudformation create-stack \
    --stack-name "${STACK_PREFIX}-security" \
    --template-body file://security.yml \
    --parameters \
        ParameterKey=Environment,ParameterValue=$ENVIRONMENT \
        ParameterKey=VpcId,ParameterValue=$VPC_ID \
    --capabilities CAPABILITY_NAMED_IAM

wait_for_stack "${STACK_PREFIX}-security"

# Deploy ECS Stack
echo "Deploying ECS stack..."
aws cloudformation create-stack \
    --stack-name "${STACK_PREFIX}-ecs" \
    --template-body file://ecs.yml \
    --parameters \
        ParameterKey=Environment,ParameterValue=$ENVIRONMENT \
        ParameterKey=VpcId,ParameterValue=$VPC_ID

wait_for_stack "${STACK_PREFIX}-ecs"

# Deploy ECS Service Stack
echo "Deploying ECS service stack..."
aws cloudformation create-stack \
    --stack-name "${STACK_PREFIX}-ecs-service" \
    --template-body file://ecs-service.yml \
    --parameters \
        ParameterKey=Environment,ParameterValue=$ENVIRONMENT \
        ParameterKey=VpcId,ParameterValue=$VPC_ID

wait_for_stack "${STACK_PREFIX}-ecs-service"

echo "Infrastructure deployment complete!" 