import pytest
from unittest.mock import Mock
from uuid import uuid4

from app.application.services import WordService
from app.domain.models import DifficultyLevel, PartOfSpeech, Word
from app.infrastructure.repositories.word_repository import WordRepositoryInterface


@pytest.fixture
def mock_word_repository():
    """Create a mock word repository"""
    return Mock(spec=WordRepositoryInterface)


@pytest.fixture
def word_service(mock_word_repository):
    """Create a word service with mock repository"""
    return WordService(mock_word_repository)


@pytest.fixture
def sample_word():
    """Create a sample word for testing"""
    return Word(
        id=uuid4(),
        word="test",
        definition="a test word",
        part_of_speech=PartOfSpeech.NOUN,
        difficulty=DifficultyLevel.BEGINNER,
        language="en",
    )


class TestWordService:
    """Unit tests for WordService"""

    def test_create_word_success(self, word_service, mock_word_repository, sample_word):
        """Test creating a word successfully"""
        # Setup
        new_word = Word(
            word="test",
            definition="a test word",
            part_of_speech=PartOfSpeech.NOUN,
            difficulty=DifficultyLevel.BEGINNER,
            language="en",
        )
        mock_word_repository.get_by_word.return_value = None
        mock_word_repository.create.return_value = sample_word
        
        # Execute
        result = word_service.create_word(new_word)
        
        # Assert
        assert result == sample_word
        mock_word_repository.get_by_word.assert_called_once_with(word="test", language="en")
        mock_word_repository.create.assert_called_once_with(word=new_word)

    def test_create_word_already_exists(self, word_service, mock_word_repository, sample_word):
        """Test creating a word that already exists"""
        # Setup
        new_word = Word(
            word="test",
            definition="a test word",
            part_of_speech=PartOfSpeech.NOUN,
            difficulty=DifficultyLevel.BEGINNER,
            language="en",
        )
        mock_word_repository.get_by_word.return_value = sample_word
        
        # Execute & Assert
        with pytest.raises(ValueError, match="Word 'test' already exists for language 'en'"):
            word_service.create_word(new_word)
        
        mock_word_repository.get_by_word.assert_called_once_with(word="test", language="en")
        mock_word_repository.create.assert_not_called()

    def test_get_word_by_id(self, word_service, mock_word_repository, sample_word):
        """Test getting a word by ID"""
        # Setup
        mock_word_repository.get_by_id.return_value = sample_word
        
        # Execute
        result = word_service.get_word_by_id(sample_word.id)
        
        # Assert
        assert result == sample_word
        mock_word_repository.get_by_id.assert_called_once_with(word_id=sample_word.id)

    def test_get_word_by_word(self, word_service, mock_word_repository, sample_word):
        """Test getting a word by word text"""
        # Setup
        mock_word_repository.get_by_word.return_value = sample_word
        
        # Execute
        result = word_service.get_word_by_word("test", "en")
        
        # Assert
        assert result == sample_word
        mock_word_repository.get_by_word.assert_called_once_with(word="test", language="en")

    def test_get_all_words(self, word_service, mock_word_repository, sample_word):
        """Test getting all words"""
        # Setup
        words_list = [sample_word]
        mock_word_repository.get_all.return_value = words_list
        
        # Execute
        result = word_service.get_all_words()
        
        # Assert
        assert result == words_list
        mock_word_repository.get_all.assert_called_once_with()

    def test_update_word_success(self, word_service, mock_word_repository, sample_word):
        """Test updating a word successfully"""
        # Setup
        mock_word_repository.get_by_id.return_value = sample_word
        mock_word_repository.update.return_value = sample_word
        
        # Execute
        result = word_service.update_word(sample_word)
        
        # Assert
        assert result == sample_word
        mock_word_repository.get_by_id.assert_called_once_with(word_id=sample_word.id)
        mock_word_repository.update.assert_called_once_with(word=sample_word)

    def test_update_word_without_id(self, word_service, mock_word_repository):
        """Test updating a word without an ID"""
        # Setup
        word_without_id = Word(
            word="test",
            definition="a test word",
            part_of_speech=PartOfSpeech.NOUN,
            difficulty=DifficultyLevel.BEGINNER,
            language="en",
        )
        
        # Execute & Assert
        with pytest.raises(ValueError, match="Word ID is required for update"):
            word_service.update_word(word_without_id)
        
        mock_word_repository.get_by_id.assert_not_called()
        mock_word_repository.update.assert_not_called()

    def test_update_word_not_found(self, word_service, mock_word_repository, sample_word):
        """Test updating a word that doesn't exist"""
        # Setup
        mock_word_repository.get_by_id.return_value = None
        
        # Execute & Assert
        with pytest.raises(ValueError, match=f"Word with ID {sample_word.id} not found"):
            word_service.update_word(sample_word)
        
        mock_word_repository.get_by_id.assert_called_once_with(word_id=sample_word.id)
        mock_word_repository.update.assert_not_called()

    def test_delete_word(self, word_service, mock_word_repository):
        """Test deleting a word"""
        # Setup
        mock_word_repository.delete.return_value = True
        
        # Execute
        result = word_service.delete_word(sample_word.id)
        
        # Assert
        assert result is True
        mock_word_repository.delete.assert_called_once_with(word_id=sample_word.id)