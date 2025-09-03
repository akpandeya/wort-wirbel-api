"""
Infrastructure layer: Database setup and configuration
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.infrastructure.config import DbConfig


class Base(DeclarativeBase):
    """Database declarative base"""
    pass


class Database:
    """Database session management"""

    def __init__(self, config: DbConfig):
        self.engine = create_engine(config.connection_string)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_session(self):
        """Get a database session"""
        session = self.SessionLocal()
        try:
            yield session
        finally:
            session.close()

    def create_tables(self):
        """Create all tables"""
        Base.metadata.create_all(bind=self.engine)


# Global database instance
_database = None


def get_database() -> Database:
    """Get the global database instance"""
    global _database
    if _database is None:
        config = DbConfig.from_env()
        _database = Database(config)
    return _database


def get_db_session():
    """Get a database session (dependency injection)"""
    return get_database().get_session()