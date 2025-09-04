#!/bin/bash

echo "Stopping PostgreSQL test container..."
docker-compose -f docker-compose.test.yml down

echo "Test database stopped and cleaned up."
