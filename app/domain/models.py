from datetime import datetime
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel


class PartOfSpeech(str, Enum):
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
    A1 = "A1"
    A2 = "A2"
    B1 = "B1"
    B2 = "B2"
    C1 = "C1"
    C2 = "C2"


class Gender(str, Enum):
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
    text: str
    tr: str


class Word(BaseModel):
    id: Optional[str] = None
    lemma: str
    lang: str
    pos: PartOfSpeech
    pos_specific: Optional[str] = None
    defs: List[str]
    synonyms: Optional[List[str]] = None
    examples: Optional[List[Example]] = None
    freq_rank: Optional[int] = None
    cefr: Optional[CEFRLevel] = None
    gender: Optional[Gender] = None
    plural: Optional[str] = None
    audio: Optional[str] = None
    src: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
