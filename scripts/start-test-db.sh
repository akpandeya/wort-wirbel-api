#!/bin/bash

# Start PostgreSQL test container
echo "Starting PostgreSQL test container..."
docker-compose -f docker-compose.test.yml up -d

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
for i in {1..30}; do
    if docker exec wort-wirbel-test-db pg_isready -U test_user -d test_wort_wirbel > /dev/null 2>&1; then
        echo "PostgreSQL is ready!"
        break
    fi
    echo "Waiting... ($i/30)"
    sleep 1
done

if [ $i -eq 30 ]; then
    echo "PostgreSQL failed to start within 30 seconds"
    exit 1
fi

echo "Test database is ready at localhost:5433"
echo "Connection string: postgresql://test_user:test_password@localhost:5433/test_wort_wirbel"
