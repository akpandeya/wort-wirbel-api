import pytest
import pytest_asyncio
from app.domain.models import Word, PartOfSpeech

from app.infrastructure.repositories.word_repository import SqlWordRepository


@pytest_asyncio.fixture
async def word_repository(db_session):
    """Create a word repository instance."""
    return SqlWordRepository(db_session)


@pytest.fixture
def sample_word():
    """Create a sample word for testing."""
    return Word(
        id="de:hallo:1",
        lemma="Hallo",
        lang="de",
        pos=PartOfSpeech.INTERJECTION,
        defs=["hello", "hi"],
    )


@pytest.mark.asyncio
async def test_create_word(word_repository, sample_word):
    """Test creating a new word in the repository."""
    created_word = await word_repository.create(sample_word)

    assert created_word.id is not None
    assert created_word.lemma == sample_word.lemma
    assert created_word.lang == sample_word.lang
    assert created_word.pos == sample_word.pos
    assert created_word.defs == sample_word.defs


@pytest.mark.asyncio
async def test_get_by_id_existing_word(word_repository, sample_word):
    """Test retrieving an existing word by ID."""
    created_word = await word_repository.create(sample_word)

    retrieved_word = await word_repository.get_by_id(created_word.id)

    assert retrieved_word is not None
    assert retrieved_word.id == created_word.id
    assert retrieved_word.lemma == created_word.lemma


@pytest.mark.asyncio
async def test_get_by_id_nonexistent_word(word_repository):
    """Test retrieving a non-existent word returns None."""
    retrieved_word = await word_repository.get_by_id("nonexistent-id")

    assert retrieved_word is None


@pytest.mark.asyncio
async def test_get_by_lemma_existing(word_repository, sample_word):
    """Test retrieving an existing word by lemma and language."""
    created_word = await word_repository.create(sample_word)

    retrieved_word = await word_repository.get_by_lemma(
        sample_word.lemma, sample_word.lang
    )

    assert retrieved_word is not None
    assert retrieved_word.id == created_word.id
    assert retrieved_word.lemma == created_word.lemma


@pytest.mark.asyncio
async def test_get_by_lemma_nonexistent(word_repository):
    """Test retrieving a non-existent word by lemma returns None."""
    retrieved_word = await word_repository.get_by_lemma("nonexistent", "en")

    assert retrieved_word is None


@pytest.mark.asyncio
async def test_get_all_empty(word_repository):
    """Test getting all words when repository is empty."""
    words = await word_repository.get_all()

    assert words == []


@pytest.mark.asyncio
async def test_get_all_with_words(word_repository, sample_word):
    """Test getting all words when repository contains words."""
    await word_repository.create(sample_word)
    word2 = Word(
        id="en:hello:2",
        lemma="Hello",
        lang="en",
        pos=PartOfSpeech.INTERJECTION,
        defs=["hi"],
    )
    await word_repository.create(word2)

    words = await word_repository.get_all()

    assert len(words) >= 2
    ids = [w.id for w in words]
    assert sample_word.id in ids
    assert word2.id in ids


@pytest.mark.asyncio
async def test_update_word(word_repository, sample_word):
    """Test updating an existing word."""
    created_word = await word_repository.create(sample_word)
    created_word.defs = ["greeting"]

    updated_word = await word_repository.update(created_word)

    assert updated_word.id == created_word.id
    assert updated_word.defs == ["greeting"]


@pytest.mark.asyncio
async def test_update_word_without_id(word_repository, sample_word):
    """Test updating a word without ID raises ValueError."""
    word_no_id = Word(
        lemma="Hallo", lang="de", pos=PartOfSpeech.INTERJECTION, defs=["hello", "hi"]
    )
    with pytest.raises(ValueError, match="Word ID is required for update"):
        await word_repository.update(word_no_id)


@pytest.mark.asyncio
async def test_update_nonexistent_word(word_repository, sample_word):
    """Test updating a non-existent word raises ValueError."""
    word_nonexistent = Word(
        id="nonexistent-id",
        lemma="Hallo",
        lang="de",
        pos=PartOfSpeech.INTERJECTION,
        defs=["hello", "hi"],
    )
    with pytest.raises(ValueError, match="Word with ID nonexistent-id not found"):
        await word_repository.update(word_nonexistent)


@pytest.mark.asyncio
async def test_delete_existing_word(word_repository, sample_word):
    """Test deleting an existing word."""
    created_word = await word_repository.create(sample_word)

    result = await word_repository.delete(created_word.id)

    assert result is True


@pytest.mark.asyncio
async def test_delete_nonexistent_word(word_repository):
    """Test deleting a non-existent word returns False."""
    result = await word_repository.delete("nonexistent-id")

    assert result is False
