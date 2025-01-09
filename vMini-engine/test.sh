#!/bin/bash

# Function to check if service is healthy
check_health() {
    curl -s http://localhost:8000/health > /dev/null
    return $?
}

# Clean up function
cleanup() {
    echo "Cleaning up..."
    docker-compose down
    exit 1
}

# Trap Ctrl+C and call cleanup
trap cleanup INT

# Ensure the container is running
if ! docker-compose ps | grep -q "Up"; then
    echo "Starting services..."
    docker-compose down  # Clean up any existing containers
    docker-compose build --no-cache  # Rebuild without cache
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
        cleanup
    fi
    echo "Attempt $count/$max_retries..."
    sleep 2
done

echo "Service is ready! Running tests..."

# Run the tests
# If no specific tests specified, run all tests
if [ $# -eq 0 ]; then
    python -m pytest src/tests/ -v
else
    # Run specified tests
    docker-compose run -T app pytest -s "$@"
fi 