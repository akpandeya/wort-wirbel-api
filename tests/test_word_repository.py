import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer
from uuid import uuid4

from app.domain.models import DifficultyLevel, PartOfSpeech, Word
from app.infrastructure.database import Base
from app.infrastructure.repositories.word_repository import SqlWordRepository


@pytest.fixture(scope="module")
def postgres_container():
    """Start a PostgreSQL container for testing"""
    with PostgresContainer("postgres:15") as postgres:
        yield postgres


@pytest.fixture(scope="module")
def database_engine(postgres_container):
    """Create a database engine connected to the test container"""
    connection_string = postgres_container.get_connection_url()
    engine = create_engine(connection_string)
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session(database_engine):
    """Create a database session for testing with transaction rollback"""
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=database_engine)
    session = SessionLocal()
    
    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture
def word_repository(db_session):
    """Create a word repository for testing"""
    return SqlWordRepository(db_session)


@pytest.fixture
def sample_word():
    """Create a sample word for testing"""
    return Word(
        word="test",
        definition="a test word",
        part_of_speech=PartOfSpeech.NOUN,
        difficulty=DifficultyLevel.BEGINNER,
        language="en",
    )


class TestSqlWordRepository:
    """Integration tests for SqlWordRepository"""

    def test_create_word(self, word_repository, sample_word):
        """Test creating a word"""
        created_word = word_repository.create(sample_word)
        
        assert created_word.id is not None
        assert isinstance(created_word.id, type(uuid4()))
        assert created_word.word == sample_word.word
        assert created_word.definition == sample_word.definition
        assert created_word.part_of_speech == sample_word.part_of_speech
        assert created_word.difficulty == sample_word.difficulty
        assert created_word.language == sample_word.language
        assert created_word.created_at is not None
        assert created_word.updated_at is not None

    def test_get_by_id_existing_word(self, word_repository, sample_word):
        """Test getting a word by ID when it exists"""
        created_word = word_repository.create(sample_word)
        
        retrieved_word = word_repository.get_by_id(created_word.id)
        
        assert retrieved_word is not None
        assert retrieved_word.id == created_word.id
        assert retrieved_word.word == created_word.word

    def test_get_by_id_nonexistent_word(self, word_repository):
        """Test getting a word by ID when it doesn't exist"""
        retrieved_word = word_repository.get_by_id(99999)
        
        assert retrieved_word is None

    def test_get_by_word_existing(self, word_repository, sample_word):
        """Test getting a word by word text and language when it exists"""
        created_word = word_repository.create(sample_word)
        
        retrieved_word = word_repository.get_by_word(sample_word.word, sample_word.language)
        
        assert retrieved_word is not None
        assert retrieved_word.id == created_word.id
        assert retrieved_word.word == created_word.word

    def test_get_by_word_nonexistent(self, word_repository):
        """Test getting a word by word text and language when it doesn't exist"""
        retrieved_word = word_repository.get_by_word("nonexistent", "en")
        
        assert retrieved_word is None

    def test_get_all_empty(self, word_repository):
        """Test getting all words when repository is empty"""
        words = word_repository.get_all()
        
        assert words == []

    def test_get_all_with_words(self, word_repository, sample_word):
        """Test getting all words when repository has words"""
        word1 = word_repository.create(sample_word)
        word2 = word_repository.create(Word(
            word="test2",
            definition="another test word",
            part_of_speech=PartOfSpeech.VERB,
            difficulty=DifficultyLevel.INTERMEDIATE,
            language="en",
        ))
        
        words = word_repository.get_all()
        
        assert len(words) == 2
        word_ids = [w.id for w in words]
        assert word1.id in word_ids
        assert word2.id in word_ids

    def test_update_word(self, word_repository, sample_word):
        """Test updating an existing word"""
        created_word = word_repository.create(sample_word)
        original_updated_at = created_word.updated_at
        
        # Update the word
        created_word.definition = "updated definition"
        created_word.difficulty = DifficultyLevel.ADVANCED
        
        updated_word = word_repository.update(created_word)
        
        assert updated_word.id == created_word.id
        assert updated_word.definition == "updated definition"
        assert updated_word.difficulty == DifficultyLevel.ADVANCED
        assert updated_word.updated_at != original_updated_at

    def test_update_word_without_id(self, word_repository, sample_word):
        """Test updating a word without an ID raises error"""
        with pytest.raises(ValueError, match="Word ID is required for update"):
            word_repository.update(sample_word)

    def test_update_nonexistent_word(self, word_repository, sample_word):
        """Test updating a word that doesn't exist raises error"""
        sample_word.id = 99999
        
        with pytest.raises(ValueError, match="Word with ID 99999 not found"):
            word_repository.update(sample_word)

    def test_delete_existing_word(self, word_repository, sample_word):
        """Test deleting an existing word"""
        created_word = word_repository.create(sample_word)
        
        result = word_repository.delete(created_word.id)
        
        assert result is True
        assert word_repository.get_by_id(created_word.id) is None

    def test_delete_nonexistent_word(self, word_repository):
        """Test deleting a word that doesn't exist"""
        result = word_repository.delete(99999)
        
        assert result is False