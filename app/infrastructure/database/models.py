"""
SQLAlchemy models for the word schema
"""

from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, Integer, String, func

from app.domain.models import DifficultyLevel, PartOfSpeech
from app.infrastructure.database import Base


class WordModel(Base):
    """SQLAlchemy model for Word table"""

    __tablename__ = "words"

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String, nullable=False, index=True)
    definition = Column(String, nullable=False)
    part_of_speech = Column(Enum(PartOfSpeech), nullable=False)
    difficulty = Column(Enum(DifficultyLevel), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)