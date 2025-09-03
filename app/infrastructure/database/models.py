"""
SQLAlchemy models for the word schema
"""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, Enum, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID

from app.domain.models import DifficultyLevel, PartOfSpeech
from app.infrastructure.database import Base


class WordModel(Base):
    """SQLAlchemy model for Word table"""

    __tablename__ = "words"
    __table_args__ = (
        UniqueConstraint('word', 'language', name='uq_word_language'),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    word = Column(String, nullable=False, index=True)
    definition = Column(String, nullable=False)
    part_of_speech = Column(Enum(PartOfSpeech), nullable=False)
    difficulty = Column(Enum(DifficultyLevel), nullable=False)
    language = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)