"""
Tests for the comprehensive Word domain model
"""

from datetime import datetime
from app.domain.models import Word, PartOfSpeech, CEFRLevel, Gender, Example


def test_word_creation_minimal():
    """Test creating a word with minimal required fields"""
    word = Word(
        lemma="Hallo",
        lang="de",
        pos=PartOfSpeech.INTERJECTION,
        defs=["hello", "hi"]
    )
    
    assert word.lemma == "Hallo"
    assert word.lang == "de"
    assert word.pos == PartOfSpeech.INTERJECTION
    assert word.defs == ["hello", "hi"]
    assert word.id is None  # Should be None if not provided


def test_word_creation_comprehensive():
    """Test creating a word with all fields"""
    examples = [
        Example(text="Hallo Welt!", tr="Hello world!"),
        Example(text="Hallo, wie geht's?", tr="Hello, how are you?")
    ]
    
    word = Word(
        id="de:hallo:abc123",
        lemma="Hallo",
        lang="de",
        pos=PartOfSpeech.INTERJECTION,
        pos_specific="Interjektion",
        defs=["hello", "hi"],
        synonyms=["hi", "guten Tag"],
        examples=examples,
        freq_rank=523,
        cefr=CEFRLevel.A1,
        gender=None,  # Interjections don't have gender
        plural=None,  # Interjections don't have plural
        audio="https://cdn.example.com/audio/de/hallo.mp3",
        src="dict-api-v1",
        success_streak=0,
        last_reviewed_at=None,
        next_review_at=None
    )
    
    assert word.id == "de:hallo:abc123"
    assert word.lemma == "Hallo"
    assert word.lang == "de"
    assert word.pos == PartOfSpeech.INTERJECTION
    assert word.pos_specific == "Interjektion"
    assert word.defs == ["hello", "hi"]
    assert word.synonyms == ["hi", "guten Tag"]
    assert len(word.examples) == 2
    assert word.examples[0].text == "Hallo Welt!"
    assert word.examples[0].tr == "Hello world!"
    assert word.freq_rank == 523
    assert word.cefr == CEFRLevel.A1
    assert word.gender is None
    assert word.plural is None
    assert word.audio == "https://cdn.example.com/audio/de/hallo.mp3"
    assert word.src == "dict-api-v1"
    assert word.success_streak == 0


def test_word_creation_with_gender():
    """Test creating a noun with gender"""
    word = Word(
        lemma="Haus",
        lang="de",
        pos=PartOfSpeech.NOUN,
        pos_specific="Substantiv",
        defs=["house", "building"],
        gender=Gender.NEUTER,
        plural="Häuser",
        cefr=CEFRLevel.A1
    )
    
    assert word.lemma == "Haus"
    assert word.gender == Gender.NEUTER
    assert word.plural == "Häuser"


def test_example_creation():
    """Test creating an Example object"""
    example = Example(
        text="Das ist ein schönes Haus.",
        tr="This is a beautiful house."
    )
    
    assert example.text == "Das ist ein schönes Haus."
    assert example.tr == "This is a beautiful house."