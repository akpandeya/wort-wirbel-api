import pytest
import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.infrastructure.database import Base
from testcontainers.postgres import PostgresContainer


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def postgres_container():
    """Start PostgreSQL container for the test session."""
    with PostgresContainer("postgres:15-alpine") as postgres:
        yield postgres.get_connection_url().replace(
            "postgresql+psycopg2", "postgresql+asyncpg"
        )


@pytest.fixture(scope="session")
async def database_engine(postgres_container):
    """Create async database engine and setup schema."""
    engine = create_async_engine(postgres_container, echo=False)

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
    """Create a database session for each test, with a nested transaction."""
    connection = await database_engine.connect()
    trans = await connection.begin()

    # bind an individual Session to the connection
    async_session = sessionmaker(
        connection, expire_on_commit=False, class_=AsyncSession
    )
    session = async_session()

    yield session

    await session.close()
    await trans.rollback()
    await connection.close()


# Configure asyncio for Windows
if os.name == "nt":  # Windows
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
