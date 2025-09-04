from sqlalchemy import Column, DateTime, Enum, String, Integer, JSON, Text, func

from app.domain.models import PartOfSpeech, CEFRLevel, Gender
from app.infrastructure.database import Base


class WordModel(Base):
    __tablename__ = "word"

    id = Column(String, primary_key=True, index=True)
    lemma = Column(String, nullable=False, index=True)
    lang = Column(String, nullable=False, index=True)
    pos = Column(Enum(PartOfSpeech), nullable=False)
    pos_specific = Column(String, nullable=True)
    defs = Column(JSON, nullable=False)
    synonyms = Column(JSON, nullable=True)
    examples = Column(JSON, nullable=True)
    freq_rank = Column(Integer, nullable=True)
    cefr = Column(Enum(CEFRLevel), nullable=True)
    gender = Column(Enum(Gender), nullable=True)
    plural = Column(String, nullable=True)
    audio = Column(Text, nullable=True)
    src = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )
