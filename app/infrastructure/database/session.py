from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.infrastructure.config import DbConfig
from . import Base


class Database:
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
        self.engine = create_async_engine(
            config.connection_string, future=True, echo=False
        )
        self.SessionLocal = async_sessionmaker(
            self.engine, expire_on_commit=False, class_=AsyncSession
        )
        self._initialized = True

    async def get_session(self):
        async with self.SessionLocal() as session:
            yield session

    async def create_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


def get_database() -> Database:
    return Database()


def get_db_session():
    return get_database().get_session()
