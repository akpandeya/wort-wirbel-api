import pytest
from unittest.mock import AsyncMock
from app.application.word_service import WordService
from app.domain.models import Word, PartOfSpeech
import pytest_asyncio


@pytest_asyncio.fixture
def mock_word_repository():
    repo = AsyncMock()
    return repo


@pytest_asyncio.fixture
def word_service(mock_word_repository):
    return WordService(mock_word_repository)


@pytest.fixture
def sample_word():
    return Word(
        id="de:hallo:1",
        lemma="Hallo",
        lang="de",
        pos=PartOfSpeech.INTERJECTION,
        defs=["hello", "hi"],
    )


@pytest.mark.asyncio
async def test_create_word_success(word_service, mock_word_repository, sample_word):
    mock_word_repository.get_by_lemma.return_value = None
    mock_word_repository.create.return_value = sample_word

    result = await word_service.create_word(sample_word)

    assert result == sample_word
    mock_word_repository.get_by_lemma.assert_awaited_once_with(
        lemma="Hallo", language="de"
    )
    mock_word_repository.create.assert_awaited_once_with(word=sample_word)


@pytest.mark.asyncio
async def test_create_word_already_exists(
    word_service, mock_word_repository, sample_word
):
    mock_word_repository.get_by_lemma.return_value = sample_word

    with pytest.raises(
        ValueError, match="Word 'Hallo' already exists for language 'de'"
    ):
        await word_service.create_word(sample_word)

    mock_word_repository.get_by_lemma.assert_awaited_once_with(
        lemma="Hallo", language="de"
    )
    mock_word_repository.create.assert_not_awaited()


@pytest.mark.asyncio
async def test_get_word_by_id(word_service, mock_word_repository, sample_word):
    mock_word_repository.get_by_id.return_value = sample_word

    result = await word_service.get_word_by_id("de:hallo:1")

    assert result == sample_word
    mock_word_repository.get_by_id.assert_awaited_once_with(word_id="de:hallo:1")


@pytest.mark.asyncio
async def test_get_word_by_lemma(word_service, mock_word_repository, sample_word):
    mock_word_repository.get_by_lemma.return_value = sample_word

    result = await word_service.get_word_by_lemma("Hallo", "de")

    assert result == sample_word
    mock_word_repository.get_by_lemma.assert_awaited_once_with(
        lemma="Hallo", language="de"
    )


@pytest.mark.asyncio
async def test_get_all_words(word_service, mock_word_repository, sample_word):
    mock_word_repository.get_all.return_value = [sample_word]

    result = await word_service.get_all_words()

    assert result == [sample_word]
    mock_word_repository.get_all.assert_awaited_once_with()


@pytest.mark.asyncio
async def test_update_word_success(word_service, mock_word_repository, sample_word):
    mock_word_repository.get_by_id.return_value = sample_word
    mock_word_repository.update.return_value = sample_word

    result = await word_service.update_word(sample_word)

    assert result == sample_word
    mock_word_repository.get_by_id.assert_awaited_once_with(word_id=sample_word.id)
    mock_word_repository.update.assert_awaited_once_with(word=sample_word)


@pytest.mark.asyncio
async def test_update_word_without_id(word_service, mock_word_repository, sample_word):
    word_no_id = Word(
        lemma="Hallo",
        lang="de",
        pos=PartOfSpeech.INTERJECTION,
        defs=["hello", "hi"],
    )

    with pytest.raises(ValueError, match="Word ID is required for update"):
        await word_service.update_word(word_no_id)

    mock_word_repository.get_by_id.assert_not_awaited()
    mock_word_repository.update.assert_not_awaited()


@pytest.mark.asyncio
async def test_update_word_not_found(word_service, mock_word_repository, sample_word):
    mock_word_repository.get_by_id.return_value = None

    with pytest.raises(ValueError, match=f"Word with ID {sample_word.id} not found"):
        await word_service.update_word(sample_word)

    mock_word_repository.get_by_id.assert_awaited_once_with(word_id=sample_word.id)
    mock_word_repository.update.assert_not_awaited()


@pytest.mark.asyncio
async def test_delete_word(word_service, mock_word_repository, sample_word):
    mock_word_repository.delete.return_value = True

    result = await word_service.delete_word(sample_word.id)

    assert result is True
    mock_word_repository.delete.assert_awaited_once_with(word_id=sample_word.id)
