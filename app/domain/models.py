from datetime import datetime
from enum import Enum
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
    OTHER = "other"


class DifficultyLevel(str, Enum):
    """Difficulty level enumeration"""

    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class ServiceInfo(BaseModel):
    message: str
    service: str
    version: str


class HealthStatus(BaseModel):
    status: str
    service: str


class Word(BaseModel):
    """Word domain model"""

    id: UUID | None = None
    word: str
    definition: str
    part_of_speech: PartOfSpeech
    difficulty: DifficultyLevel
    language: str
    created_at: datetime | None = None
    updated_at: datetime | None = None
