#!/bin/bash

# Default to development if no environment specified
export ENVIRONMENT=${ENVIRONMENT:-development}

# Create necessary directories if they don't exist
mkdir -p output logs

echo "Starting application in $ENVIRONMENT mode..."

# Build and run the Docker containers
docker-compose up --build 