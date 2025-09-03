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
    """Database session management with singleton pattern"""
    
    _instance = None
    _lock = None

    def __new__(cls, config: DbConfig = None):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, config: DbConfig = None):
        if self._initialized:
            return
        
        if config is None:
            config = DbConfig.from_env()
            
        self.engine = create_engine(config.connection_string)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self._initialized = True

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


def get_database() -> Database:
    """Get the database instance (singleton)"""
    return Database()


def get_db_session():
    """Get a database session (dependency injection)"""
    return get_database().get_session()