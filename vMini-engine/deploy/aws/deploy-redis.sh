#!/bin/bash

# Get VPC and subnet IDs
VPC_ID=$(aws ec2 describe-vpcs --filters "Name=tag:Name,Values=vMini-engine-vpc" --query "Vpcs[0].VpcId" --output text)
SUBNET_IDS=$(aws ec2 describe-subnets --filters "Name=vpc-id,Values=$VPC_ID" --query "Subnets[*].SubnetId" --output text | tr '\t' ',')

STACK_NAME="vmini-engine-redis"

# Check if stack exists
if aws cloudformation describe-stacks --stack-name $STACK_NAME >/dev/null 2>&1; then
    echo "Updating existing Redis stack..."
    
    # Update existing stack
    aws cloudformation update-stack \
        --stack-name $STACK_NAME \
        --template-body file://deploy/aws/redis.yml \
        --parameters \
            ParameterKey=VpcId,ParameterValue=$VPC_ID \
            ParameterKey=SubnetIds,ParameterValue=\"$SUBNET_IDS\" \
        --capabilities CAPABILITY_IAM

    echo "Waiting for Redis stack update to complete..."
    aws cloudformation wait stack-update-complete --stack-name $STACK_NAME
else
    echo "Creating new Redis stack..."
    
    # Create new stack
    aws cloudformation create-stack \
        --stack-name $STACK_NAME \
        --template-body file://deploy/aws/redis.yml \
        --parameters \
            ParameterKey=VpcId,ParameterValue=$VPC_ID \
            ParameterKey=SubnetIds,ParameterValue=\"$SUBNET_IDS\" \
        --capabilities CAPABILITY_IAM

    echo "Waiting for Redis stack creation to complete..."
    aws cloudformation wait stack-create-complete --stack-name $STACK_NAME
fi

# Get Redis endpoint
REDIS_ENDPOINT=$(aws cloudformation describe-stacks \
    --stack-name $STACK_NAME \
    --query 'Stacks[0].Outputs[?OutputKey==`RedisEndpoint`].OutputValue' \
    --output text)

REDIS_PORT=$(aws cloudformation describe-stacks \
    --stack-name $STACK_NAME \
    --query 'Stacks[0].Outputs[?OutputKey==`RedisPort`].OutputValue' \
    --output text)

# Update environment variables
sed -i '' "s/REDIS_HOST=.*/REDIS_HOST=$REDIS_ENDPOINT/" .env.production
sed -i '' "s/REDIS_PORT=.*/REDIS_PORT=$REDIS_PORT/" .env.production

echo "Redis deployment complete!"
echo "Endpoint: $REDIS_ENDPOINT"
echo "Port: $REDIS_PORT" 