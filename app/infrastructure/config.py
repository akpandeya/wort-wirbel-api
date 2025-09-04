"""
Infrastructure layer: Configuration classes
"""

import os
from dataclasses import dataclass


@dataclass
class DbConfig:
    """Database configuration"""

    host: str
    port: int
    database: str
    username: str
    password: str

    @classmethod
    def from_env(cls) -> "DbConfig":
        """Create DbConfig from environment variables"""
        return cls(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "5432")),
            database=os.getenv("DB_NAME", "wort_wirbel"),
            username=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "postgres"),
        )

    @property
    def connection_string(self) -> str:
        """Get the async database connection string for SQLAlchemy async engine"""
        return f"postgresql+asyncpg://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
