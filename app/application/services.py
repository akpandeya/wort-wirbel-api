from typing import List, Optional

from app import __version__
from app.domain.models import HealthStatus, ServiceInfo, Word
from app.infrastructure.repositories.word_repository import WordRepositoryInterface


class InfoService:
    @staticmethod
    def get_service_info() -> ServiceInfo:
        return ServiceInfo(
            message="Hello World", service="wort-wirbel-api", version=__version__
        )


class HealthService:
    @staticmethod
    def get_health_status() -> HealthStatus:
        return HealthStatus(status="healthy", service="wort-wirbel-api")


class WordService:
    """Application service for word management"""

    def __init__(self, word_repository: WordRepositoryInterface):
        self.word_repository = word_repository

    def create_word(self, word: Word) -> Word:
        """Create a new word"""
        # Check if word already exists for the same language
        existing_word = self.word_repository.get_by_lemma(lemma=word.lemma, language=word.lang)
        if existing_word:
            raise ValueError(f"Word '{word.lemma}' already exists for language '{word.lang}'")
        
        return self.word_repository.create(word=word)

    def get_word_by_id(self, word_id: str) -> Optional[Word]:
        """Get a word by ID"""
        return self.word_repository.get_by_id(word_id=word_id)

    def get_word_by_lemma(self, lemma: str, language: str) -> Optional[Word]:
        """Get a word by lemma and language"""
        return self.word_repository.get_by_lemma(lemma=lemma, language=language)

    def get_all_words(self) -> List[Word]:
        """Get all words"""
        return self.word_repository.get_all()

    def update_word(self, word: Word) -> Word:
        """Update an existing word"""
        if not word.id:
            raise ValueError("Word ID is required for update")
        
        # Check if word exists
        existing_word = self.word_repository.get_by_id(word_id=word.id)
        if not existing_word:
            raise ValueError(f"Word with ID {word.id} not found")
        
        return self.word_repository.update(word=word)

    def delete_word(self, word_id: str) -> bool:
        """Delete a word by ID"""
        return self.word_repository.delete(word_id=word_id)
