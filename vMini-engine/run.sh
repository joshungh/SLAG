#!/bin/bash

# Create necessary directories if they don't exist
mkdir -p output logs

# Build and run the Docker containers
docker-compose up --build 