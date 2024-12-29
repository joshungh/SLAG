#!/bin/bash

# Build and run tests in Docker
docker-compose -f docker/docker-compose.yml run --rm test 