from datetime import datetime
from enum import Enum

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

    id: int | None = None
    word: str
    definition: str
    part_of_speech: PartOfSpeech
    difficulty: DifficultyLevel
    updated_at: datetime | None = None
