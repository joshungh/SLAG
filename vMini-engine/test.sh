#!/bin/bash

# Function to check if service is healthy
check_health() {
    curl -s http://localhost:8000/health > /dev/null
    return $?
}

# Ensure the container is running
if ! docker-compose ps | grep -q "Up"; then
    echo "Starting services..."
    docker-compose up -d
fi

# Wait for service to be ready
echo "Waiting for service to be ready..."
max_retries=30
count=0
while ! check_health; do
    count=$((count + 1))
    if [ $count -eq $max_retries ]; then
        echo "Service failed to start after $max_retries attempts"
        docker-compose logs app  # Print app logs for debugging
        exit 1
    fi
    echo "Attempt $count/$max_retries..."
    sleep 2
done

echo "Service is ready! Running tests..."

# Run the test
python -m src.tests.test_world_generation 