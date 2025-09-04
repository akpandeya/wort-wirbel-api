import pytest
import asyncio
import subprocess
import time
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.infrastructure.database import Base


def is_docker_running():
    """Check if Docker is running."""
    try:
        subprocess.run(["docker", "info"], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def start_test_postgres():
    """Start PostgreSQL test container using Docker Compose."""
    if not is_docker_running():
        raise RuntimeError(
            "Docker is not running. Please start Docker before running tests."
        )

    # Stop any existing container
    subprocess.run(
        ["docker-compose", "-f", "docker-compose.test.yml", "down"], capture_output=True
    )

    # Start the container
    result = subprocess.run(
        ["docker-compose", "-f", "docker-compose.test.yml", "up", "-d"],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(f"Failed to start PostgreSQL container: {result.stderr}")

    # Wait for the database to be ready
    max_retries = 30
    for i in range(max_retries):
        try:
            result = subprocess.run(
                [
                    "docker",
                    "exec",
                    "wort-wirbel-test-db",
                    "pg_isready",
                    "-U",
                    "test_user",
                    "-d",
                    "test_wort_wirbel",
                ],
                capture_output=True,
            )
            if result.returncode == 0:
                return
        except subprocess.CalledProcessError:
            pass
        time.sleep(1)

    raise RuntimeError("PostgreSQL container failed to start within 30 seconds")


def stop_test_postgres():
    """Stop PostgreSQL test container."""
    subprocess.run(
        ["docker-compose", "-f", "docker-compose.test.yml", "down"], capture_output=True
    )


@pytest.fixture(scope="session")
def postgres_container():
    """Start PostgreSQL container for the test session."""
    start_test_postgres()
    yield {
        "host": "localhost",
        "port": 5433,
        "database": "test_wort_wirbel",
        "username": "test_user",
        "password": "test_password",
    }
    stop_test_postgres()


@pytest.fixture(scope="session")
async def database_engine(postgres_container):
    """Create async database engine and setup schema."""
    connection_string = (
        f"postgresql+asyncpg://{postgres_container['username']}:"
        f"{postgres_container['password']}@{postgres_container['host']}:"
        f"{postgres_container['port']}/{postgres_container['database']}"
    )

    engine = create_async_engine(connection_string, echo=False)

    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    # Cleanup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture
async def db_session(database_engine):
    """Create a database session for each test."""
    async_session = sessionmaker(
        database_engine, expire_on_commit=False, class_=AsyncSession
    )
    async with async_session() as session:
        yield session
        await session.rollback()


# Configure asyncio for Windows
if os.name == "nt":  # Windows
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
