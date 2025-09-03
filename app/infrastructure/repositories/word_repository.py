"""
Infrastructure layer: Repository implementations
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from app.domain.models import DifficultyLevel, PartOfSpeech, Word
from app.infrastructure.database.models import WordModel


class WordRepositoryInterface(ABC):
    """Abstract base class for Word repository"""

    @abstractmethod
    def create(self, word: Word) -> Word:
        """Create a new word"""
        pass

    @abstractmethod
    def get_by_id(self, word_id: int) -> Optional[Word]:
        """Get a word by ID"""
        pass

    @abstractmethod
    def get_by_word(self, word: str) -> Optional[Word]:
        """Get a word by the word text"""
        pass

    @abstractmethod
    def get_all(self) -> List[Word]:
        """Get all words"""
        pass

    @abstractmethod
    def update(self, word: Word) -> Word:
        """Update an existing word"""
        pass

    @abstractmethod
    def delete(self, word_id: int) -> bool:
        """Delete a word by ID"""
        pass


class SqlWordRepository(WordRepositoryInterface):
    """SQLAlchemy implementation of Word repository"""

    def __init__(self, session: Session):
        self.session = session

    def create(self, word: Word) -> Word:
        """Create a new word"""
        db_word = WordModel(
            word=word.word,
            definition=word.definition,
            part_of_speech=word.part_of_speech,
            difficulty=word.difficulty,
        )
        self.session.add(db_word)
        self.session.commit()
        self.session.refresh(db_word)
        
        return self._to_domain_model(db_word)

    def get_by_id(self, word_id: int) -> Optional[Word]:
        """Get a word by ID"""
        db_word = self.session.query(WordModel).filter(WordModel.id == word_id).first()
        return self._to_domain_model(db_word) if db_word else None

    def get_by_word(self, word: str) -> Optional[Word]:
        """Get a word by the word text"""
        db_word = self.session.query(WordModel).filter(WordModel.word == word).first()
        return self._to_domain_model(db_word) if db_word else None

    def get_all(self) -> List[Word]:
        """Get all words"""
        db_words = self.session.query(WordModel).all()
        return [self._to_domain_model(db_word) for db_word in db_words]

    def update(self, word: Word) -> Word:
        """Update an existing word"""
        if word.id is None:
            raise ValueError("Word ID is required for update")
        
        db_word = self.session.query(WordModel).filter(WordModel.id == word.id).first()
        if not db_word:
            raise ValueError(f"Word with ID {word.id} not found")
        
        db_word.word = word.word
        db_word.definition = word.definition
        db_word.part_of_speech = word.part_of_speech
        db_word.difficulty = word.difficulty
        db_word.updated_at = datetime.now(datetime.UTC).replace(tzinfo=None)
        
        self.session.commit()
        self.session.refresh(db_word)
        
        return self._to_domain_model(db_word)

    def delete(self, word_id: int) -> bool:
        """Delete a word by ID"""
        db_word = self.session.query(WordModel).filter(WordModel.id == word_id).first()
        if not db_word:
            return False
        
        self.session.delete(db_word)
        self.session.commit()
        return True

    def _to_domain_model(self, db_word: WordModel) -> Word:
        """Convert SQLAlchemy model to domain model"""
        return Word(
            id=db_word.id,
            word=db_word.word,
            definition=db_word.definition,
            part_of_speech=db_word.part_of_speech,
            difficulty=db_word.difficulty,
            updated_at=db_word.updated_at,
        )