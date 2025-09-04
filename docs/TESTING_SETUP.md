# Docker-Based Testing Setup

This project now uses Docker-based PostgreSQL testing instead of testcontainers for better async protocol support.

## Prerequisites

- Docker and Docker Compose installed and running
- Poetry for dependency management

## Quick Start

1. **Start the test database:**
   ```bash
   # On Windows
   scripts\start-test-db.bat
   
   # On Linux/macOS
   ./scripts/start-test-db.sh
   ```

2. **Run tests:**
   ```bash
   poetry run pytest
   ```

3. **Stop the test database:**
   ```bash
   # On Windows
   scripts\stop-test-db.bat
   
   # On Linux/macOS
   ./scripts/stop-test-db.sh
   ```

## How It Works

The testing setup uses:

- **Docker Compose**: Manages a PostgreSQL 15 container specifically for testing
- **Dedicated Test Port**: Uses port 5433 to avoid conflicts with local PostgreSQL
- **Isolated Database**: Each test session gets a clean database schema
- **Session-scoped Fixtures**: Database engine is created once per test session
- **Transaction Rollback**: Each test runs in a transaction that's rolled back

## Test Database Configuration

- **Host**: localhost
- **Port**: 5433
- **Database**: test_wort_wirbel
- **Username**: test_user
- **Password**: test_password

## Benefits Over Testcontainers

1. **Full Async Support**: No limitations with async protocols
2. **Better Performance**: Container reuse across test sessions
3. **Easier Debugging**: Direct connection to test database
4. **More Control**: Full Docker Compose configuration
5. **Windows Compatibility**: Better support for Windows development

## Automatic Setup

The `conftest.py` file automatically:
- Starts the PostgreSQL container before tests
- Creates the database schema
- Provides clean database sessions for each test
- Cleans up after test completion
- Stops the container when done

## Manual Database Management

You can also manage the test database manually:

```bash
# Start test database
docker-compose -f docker-compose.test.yml up -d

# Connect to test database
docker exec -it wort-wirbel-test-db psql -U test_user -d test_wort_wirbel

# Stop and remove test database
docker-compose -f docker-compose.test.yml down
```

## Troubleshooting

**Container won't start:**
- Ensure Docker is running
- Check if port 5433 is available
- Try `docker-compose -f docker-compose.test.yml down` first

**Tests fail with connection errors:**
- Wait a few seconds for PostgreSQL to fully start
- Check container logs: `docker logs wort-wirbel-test-db`

**Permission errors on scripts:**
- On Linux/macOS: `chmod +x scripts/*.sh`
