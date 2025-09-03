from datetime import datetime
from enum import Enum
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel


class PartOfSpeech(str, Enum):
    """Part of speech enumeration"""

    NOUN = "noun"
    VERB = "verb"
    ADJECTIVE = "adjective"
    ADVERB = "adverb"
    PRONOUN = "pronoun"
    PREPOSITION = "preposition"
    CONJUNCTION = "conjunction"
    INTERJECTION = "interjection"
    ARTICLE = "article"
    DETERMINER = "determiner"
    PARTICLE = "particle"
    OTHER = "other"


class CEFRLevel(str, Enum):
    """Common European Framework of Reference for Languages levels"""
    
    A1 = "A1"
    A2 = "A2"
    B1 = "B1"
    B2 = "B2"
    C1 = "C1"
    C2 = "C2"


class Gender(str, Enum):
    """Grammatical gender enumeration"""
    
    MASCULINE = "masculine"
    FEMININE = "feminine"
    NEUTER = "neuter"


class ServiceInfo(BaseModel):
    message: str
    service: str
    version: str


class HealthStatus(BaseModel):
    status: str
    service: str


class Example(BaseModel):
    """Example usage of a word with translation"""
    
    text: str
    tr: str  # translation


class Word(BaseModel):
    """Word domain model following the comprehensive schema from issue #33"""

    # Core identification
    id: Optional[str] = None  # Format: "{lang}:{lemma}:{variant_id}"
    lemma: str  # Canonical form of the word
    lang: str  # Language code (e.g., "de", "en")
    
    # Part of speech information
    pos: PartOfSpeech
    pos_specific: Optional[str] = None  # Language-specific POS (e.g., "Interjektion")
    
    # Definitions and synonyms
    defs: List[str]  # Array of definitions
    synonyms: Optional[List[str]] = None  # Array of synonyms
    
    # Examples
    examples: Optional[List[Example]] = None  # Array of usage examples
    
    # Difficulty and frequency
    freq_rank: Optional[int] = None  # Frequency ranking
    cefr: Optional[CEFRLevel] = None  # CEFR level
    
    # Grammatical information
    gender: Optional[Gender] = None  # Grammatical gender
    plural: Optional[str] = None  # Plural form
    
    # Media and source
    audio: Optional[str] = None  # Audio URL
    src: Optional[str] = None  # Source (e.g., "dict-api-v1")
    
    # Learning progress fields
    success_streak: Optional[int] = None  # Number of consecutive correct answers
    last_reviewed_at: Optional[datetime] = None  # Last time this word was reviewed
    next_review_at: Optional[datetime] = None  # Next scheduled review time
    
    # Temporal tracking
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
