#!/bin/bash

# Set variables
ENVIRONMENT="production"
AWS_REGION="us-west-2"
VPC_ID="vpc-084087a335373ed6c"
SUBNET_1="subnet-08e2f4a63424670d9"  # Your existing subnet
SUBNET_2="subnet-07754accd2f3042f7"  # Your second subnet

# Deploy Redis Stack
echo "Deploying Redis stack..."
aws cloudformation create-stack \
    --stack-name "vMini-engine-redis" \
    --template-body file://redis.yml \
    --parameters \
        ParameterKey=Environment,ParameterValue=$ENVIRONMENT \
        ParameterKey=VpcId,ParameterValue=$VPC_ID \
        ParameterKey=PrivateSubnet1,ParameterValue=$SUBNET_1 \
        ParameterKey=PrivateSubnet2,ParameterValue=$SUBNET_2

echo "Waiting for Redis stack to complete..."
aws cloudformation wait stack-create-complete --stack-name "vMini-engine-redis"

echo "Redis deployment complete!" 