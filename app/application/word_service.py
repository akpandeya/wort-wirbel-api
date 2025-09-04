from typing import List, Optional
from app.domain.models import Word
from app.infrastructure.repositories.word_repository import WordRepositoryInterface


class WordService:
    def __init__(self, word_repository: WordRepositoryInterface):
        self.word_repository = word_repository

    async def create_word(self, word: Word) -> Word:
        existing_word = await self.word_repository.get_by_lemma(
            lemma=word.lemma, language=word.lang
        )
        if existing_word:
            raise ValueError(
                f"Word '{word.lemma}' already exists for language '{word.lang}'"
            )
        return await self.word_repository.create(word=word)

    async def get_word_by_id(self, word_id: str) -> Optional[Word]:
        return await self.word_repository.get_by_id(word_id=word_id)

    async def get_word_by_lemma(self, lemma: str, language: str) -> Optional[Word]:
        return await self.word_repository.get_by_lemma(lemma=lemma, language=language)

    async def get_all_words(self) -> List[Word]:
        return await self.word_repository.get_all()

    async def update_word(self, word: Word) -> Word:
        if not word.id:
            raise ValueError("Word ID is required for update")
        existing_word = await self.word_repository.get_by_id(word_id=word.id)
        if not existing_word:
            raise ValueError(f"Word with ID {word.id} not found")
        return await self.word_repository.update(word=word)

    async def delete_word(self, word_id: str) -> bool:
        return await self.word_repository.delete(word_id=word_id)
