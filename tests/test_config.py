import os

from app.infrastructure.config import DbConfig


class TestDbConfig:
    def test_from_env_with_defaults(self):
        env_vars = ["DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASSWORD"]
        original_values = {}
        for var in env_vars:
            original_values[var] = os.environ.get(var)
            if var in os.environ:
                del os.environ[var]
        try:
            config = DbConfig.from_env()
            assert config.host == "localhost"
            assert config.port == 5432
            assert config.database == "postgres"
            assert config.username == "postgres"
            assert config.password == "postgres"
        finally:
            for var, value in original_values.items():
                if value is not None:
                    os.environ[var] = value

    def test_from_env_with_custom_values(self):
        custom_values = {
            "DB_HOST": "custom-host",
            "DB_PORT": "9999",
            "DB_NAME": "custom_db",
            "DB_USER": "custom_user",
            "DB_PASSWORD": "custom_password",
        }
        original_values = {}
        for var in custom_values:
            original_values[var] = os.environ.get(var)
            os.environ[var] = custom_values[var]
        try:
            config = DbConfig.from_env()
            assert config.host == "custom-host"
            assert config.port == 9999
            assert config.database == "custom_db"
            assert config.username == "custom_user"
            assert config.password == "custom_password"
        finally:
            for var, value in original_values.items():
                if value is not None:
                    os.environ[var] = value
                else:
                    del os.environ[var]

    def test_connection_string(self):
        config = DbConfig(
            host="localhost",
            port=5432,
            database="test_db",
            username="test_user",
            password="test_password",
        )

        expected = "postgresql+asyncpg://test_user:test_password@localhost:5432/test_db"
        assert config.connection_string == expected
