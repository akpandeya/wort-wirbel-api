"""
Infrastructure layer: Repository implementations
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models import Word, Example
from app.infrastructure.database.models import WordModel


class WordRepositoryInterface(ABC):
    @abstractmethod
    async def create(self, word: Word) -> Word:
        pass

    @abstractmethod
    async def get_by_id(self, word_id: str) -> Optional[Word]:
        pass

    @abstractmethod
    async def get_by_lemma(self, lemma: str, language: str) -> Optional[Word]:
        pass

    @abstractmethod
    async def get_all(self) -> List[Word]:
        pass

    @abstractmethod
    async def update(self, word: Word) -> Word:
        pass

    @abstractmethod
    async def delete(self, word_id: str) -> bool:
        pass


class SqlWordRepository(WordRepositoryInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, word: Word) -> Word:
        if not word.id:
            word.id = self._generate_id(word.lang, word.lemma)
        examples_json = None
        if word.examples:
            examples_json = [{"text": ex.text, "tr": ex.tr} for ex in word.examples]
        db_word = WordModel(
            id=word.id,
            lemma=word.lemma,
            lang=word.lang,
            pos=word.pos,
            pos_specific=word.pos_specific,
            defs=word.defs,
            synonyms=word.synonyms,
            examples=examples_json,
            freq_rank=word.freq_rank,
            cefr=word.cefr,
            gender=word.gender,
            plural=word.plural,
            audio=word.audio,
            src=word.src,
            success_streak=word.success_streak,
            last_reviewed_at=word.last_reviewed_at,
            next_review_at=word.next_review_at,
        )
        self.session.add(db_word)
        await self.session.commit()
        await self.session.refresh(db_word)
        return self._to_domain_model(db_word)

    async def get_by_id(self, word_id: str) -> Optional[Word]:
        result = await self.session.get(WordModel, word_id)
        return self._to_domain_model(result) if result else None

    async def get_by_lemma(self, lemma: str, language: str) -> Optional[Word]:
        from sqlalchemy import select

        stmt = select(WordModel).where(
            WordModel.lemma == lemma, WordModel.lang == language
        )
        result = await self.session.execute(stmt)
        db_word = result.scalar_one_or_none()
        return self._to_domain_model(db_word) if db_word else None

    async def get_all(self) -> List[Word]:
        from sqlalchemy import select

        stmt = select(WordModel)
        result = await self.session.execute(stmt)
        db_words = result.scalars().all()
        return [self._to_domain_model(db_word) for db_word in db_words]

    async def update(self, word: Word) -> Word:
        if not word.id:
            raise ValueError("Word ID is required for update")
        db_word = await self.session.get(WordModel, word.id)
        if not db_word:
            raise ValueError(f"Word with ID {word.id} not found")
        examples_json = None
        if word.examples:
            examples_json = [{"text": ex.text, "tr": ex.tr} for ex in word.examples]
        db_word.lemma = word.lemma
        db_word.lang = word.lang
        db_word.pos = word.pos
        db_word.pos_specific = word.pos_specific
        db_word.defs = word.defs
        db_word.synonyms = word.synonyms
        db_word.examples = examples_json
        db_word.freq_rank = word.freq_rank
        db_word.cefr = word.cefr
        db_word.gender = word.gender
        db_word.plural = word.plural
        db_word.audio = word.audio
        db_word.src = word.src
        db_word.success_streak = word.success_streak
        db_word.last_reviewed_at = word.last_reviewed_at
        db_word.next_review_at = word.next_review_at
        db_word.updated_at = datetime.now().replace(tzinfo=None)
        await self.session.commit()
        await self.session.refresh(db_word)
        return self._to_domain_model(db_word)

    async def delete(self, word_id: str) -> bool:
        db_word = await self.session.get(WordModel, word_id)
        if not db_word:
            return False
        await self.session.delete(db_word)
        await self.session.commit()
        return True

    def _generate_id(self, lang: str, lemma: str) -> str:
        return f"{lang}:{lemma}:{str(uuid4())[:8]}"

    def _to_domain_model(self, db_word: WordModel) -> Word:
        examples = None
        if db_word.examples:
            examples = [
                Example(text=ex["text"], tr=ex["tr"]) for ex in db_word.examples
            ]
        return Word(
            id=db_word.id,
            lemma=db_word.lemma,
            lang=db_word.lang,
            pos=db_word.pos,
            pos_specific=db_word.pos_specific,
            defs=db_word.defs,
            synonyms=db_word.synonyms,
            examples=examples,
            freq_rank=db_word.freq_rank,
            cefr=db_word.cefr,
            gender=db_word.gender,
            plural=db_word.plural,
            audio=db_word.audio,
            src=db_word.src,
            success_streak=db_word.success_streak,
            last_reviewed_at=db_word.last_reviewed_at,
            next_review_at=db_word.next_review_at,
            created_at=db_word.created_at,
            updated_at=db_word.updated_at,
        )
