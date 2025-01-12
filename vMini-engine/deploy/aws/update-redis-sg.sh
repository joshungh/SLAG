#!/bin/bash

# Get the App Security Group ID
APP_SG_ID=$(aws cloudformation describe-stacks \
    --stack-name vMini-engine-security \
    --query 'Stacks[0].Outputs[?ExportName==`vMini-engine-security-AppSecurityGroupId`].OutputValue' \
    --output text)

# Update Redis Security Group
aws ec2 authorize-security-group-ingress \
    --group-id sg-0b0664e5fa92bbb6d \
    --protocol tcp \
    --port 6379 \
    --source-group $APP_SG_ID 