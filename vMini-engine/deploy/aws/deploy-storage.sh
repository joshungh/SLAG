#!/bin/bash

# Set variables
ENVIRONMENT="production"
AWS_REGION="us-west-2"
STACK_PREFIX="vMini-engine"

echo "Deploying storage stack..."
aws cloudformation deploy \
    --template-file storage.yml \
    --stack-name "${STACK_PREFIX}-storage" \
    --parameter-overrides Environment=$ENVIRONMENT \
    --region $AWS_REGION

echo "Storage deployment complete!" 