"""
SQLAlchemy models for the comprehensive word schema
"""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, Enum, String, Integer, JSON, Text, func
from sqlalchemy.dialects.postgresql import UUID

from app.domain.models import PartOfSpeech, CEFRLevel, Gender
from app.infrastructure.database import Base


class WordModel(Base):
    """SQLAlchemy model for Word table following comprehensive schema"""

    __tablename__ = "words"

    # Core identification
    id = Column(String, primary_key=True, index=True)  # Format: {lang}:{lemma}:{variant_id}
    lemma = Column(String, nullable=False, index=True)  # Canonical form
    lang = Column(String, nullable=False, index=True)  # Language code
    
    # Part of speech information
    pos = Column(Enum(PartOfSpeech), nullable=False)
    pos_specific = Column(String, nullable=True)  # Language-specific POS
    
    # Definitions and synonyms (stored as JSON arrays)
    defs = Column(JSON, nullable=False)  # Array of definitions
    synonyms = Column(JSON, nullable=True)  # Array of synonyms
    
    # Examples (stored as JSON array of objects)
    examples = Column(JSON, nullable=True)  # Array of {text, tr} objects
    
    # Difficulty and frequency
    freq_rank = Column(Integer, nullable=True)  # Frequency ranking
    cefr = Column(Enum(CEFRLevel), nullable=True)  # CEFR level
    
    # Grammatical information
    gender = Column(Enum(Gender), nullable=True)  # Grammatical gender
    plural = Column(String, nullable=True)  # Plural form
    
    # Media and source
    audio = Column(Text, nullable=True)  # Audio URL
    src = Column(String, nullable=True)  # Source identifier
    
    # Learning progress fields
    success_streak = Column(Integer, default=0, nullable=True)
    last_reviewed_at = Column(DateTime, nullable=True)
    next_review_at = Column(DateTime, nullable=True)
    
    # Temporal tracking
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)