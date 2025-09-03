import pytest
from unittest.mock import Mock, patch

from app.infrastructure.config import DbConfig
from app.infrastructure.database import Database, get_database, get_db_session


class TestDatabase:
    """Tests for Database class"""

    @patch("app.infrastructure.database.create_engine")
    @patch("app.infrastructure.database.sessionmaker")
    def test_database_init(self, mock_sessionmaker, mock_create_engine):
        """Test Database initialization"""
        config = DbConfig(
            host="localhost",
            port=5432,
            database="test_db",
            username="test_user",
            password="test_password",
        )
        
        mock_engine = Mock()
        mock_create_engine.return_value = mock_engine
        mock_session_class = Mock()
        mock_sessionmaker.return_value = mock_session_class
        
        database = Database(config)
        
        mock_create_engine.assert_called_once_with(config.connection_string)
        mock_sessionmaker.assert_called_once_with(
            autocommit=False, autoflush=False, bind=mock_engine
        )
        assert database.engine == mock_engine
        assert database.SessionLocal == mock_session_class

    @patch("app.infrastructure.database.create_engine")
    @patch("app.infrastructure.database.sessionmaker")
    def test_get_session(self, mock_sessionmaker, mock_create_engine):
        """Test get_session method"""
        config = DbConfig(
            host="localhost",
            port=5432,
            database="test_db",
            username="test_user",
            password="test_password",
        )
        
        mock_engine = Mock()
        mock_create_engine.return_value = mock_engine
        mock_session_instance = Mock()
        mock_session_class = Mock(return_value=mock_session_instance)
        mock_sessionmaker.return_value = mock_session_class
        
        database = Database(config)
        
        # Test the generator
        session_generator = database.get_session()
        session = next(session_generator)
        
        assert session == mock_session_instance
        mock_session_class.assert_called_once()
        
        # Test cleanup
        try:
            next(session_generator)
        except StopIteration:
            mock_session_instance.close.assert_called_once()

    @patch("app.infrastructure.database.Base")
    @patch("app.infrastructure.database.create_engine")
    @patch("app.infrastructure.database.sessionmaker")
    def test_create_tables(self, mock_sessionmaker, mock_create_engine, mock_base):
        """Test create_tables method"""
        config = DbConfig(
            host="localhost",
            port=5432,
            database="test_db",
            username="test_user",
            password="test_password",
        )
        
        mock_engine = Mock()
        mock_create_engine.return_value = mock_engine
        mock_metadata = Mock()
        mock_base.metadata = mock_metadata
        
        database = Database(config)
        database.create_tables()
        
        mock_metadata.create_all.assert_called_once_with(bind=mock_engine)


class TestGlobalFunctions:
    """Tests for global database functions"""

    @patch("app.infrastructure.database.DbConfig")
    @patch("app.infrastructure.database.Database")
    def test_get_database_singleton(self, mock_database_class, mock_config_class):
        """Test get_database returns singleton instance"""
        mock_config = Mock()
        mock_config_class.from_env.return_value = mock_config
        mock_database_instance = Mock()
        mock_database_class.return_value = mock_database_instance
        
        # Clear the global variable first
        import app.infrastructure.database
        app.infrastructure.database._database = None
        
        # First call should create instance
        result1 = get_database()
        mock_config_class.from_env.assert_called_once()
        mock_database_class.assert_called_once_with(mock_config)
        assert result1 == mock_database_instance
        
        # Second call should return same instance
        result2 = get_database()
        assert result2 == mock_database_instance
        # Config and Database should not be called again
        assert mock_config_class.from_env.call_count == 1
        assert mock_database_class.call_count == 1

    @patch("app.infrastructure.database.get_database")
    def test_get_db_session(self, mock_get_database):
        """Test get_db_session function"""
        mock_database = Mock()
        mock_session_generator = Mock()
        mock_database.get_session.return_value = mock_session_generator
        mock_get_database.return_value = mock_database
        
        result = get_db_session()
        
        mock_get_database.assert_called_once()
        mock_database.get_session.assert_called_once()
        assert result == mock_session_generator