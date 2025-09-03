"""
Test that demonstrates the comprehensive Word schema matches the spec from issue #33
"""

import json
from datetime import datetime
from app.domain.models import Word, PartOfSpeech, CEFRLevel, Example


def test_word_matches_issue_33_spec():
    """Test that Word model can represent the JSON example from issue #33"""
    
    # Create a word that matches the example from the issue
    examples = [Example(text="Hallo Welt!", tr="Hello world!")]
    
    word = Word(
        id="de:hallo:1",
        lemma="Hallo",
        lang="de",
        pos=PartOfSpeech.INTERJECTION,
        pos_specific="Interjektion",
        defs=["hello", "hi"],
        synonyms=["hi", "guten Tag"],
        examples=examples,
        freq_rank=523,
        cefr=CEFRLevel.A1,
        gender=None,
        plural=None,
        audio="https://cdn.example.com/audio/de/hallo.mp3",
        src="dict-api-v1",
        updated_at=datetime.fromisoformat("2025-09-01T12:44:00")
    )
    
    # Verify all fields match the specification
    assert word.id == "de:hallo:1"
    assert word.lemma == "Hallo"
    assert word.lang == "de"
    assert word.pos == PartOfSpeech.INTERJECTION
    assert word.pos_specific == "Interjektion"
    assert word.defs == ["hello", "hi"]
    assert word.synonyms == ["hi", "guten Tag"]
    assert len(word.examples) == 1
    assert word.examples[0].text == "Hallo Welt!"
    assert word.examples[0].tr == "Hello world!"
    assert word.freq_rank == 523
    assert word.cefr == CEFRLevel.A1
    assert word.gender is None
    assert word.plural is None
    assert word.audio == "https://cdn.example.com/audio/de/hallo.mp3"
    assert word.src == "dict-api-v1"
    
    # Test that the model can be serialized to dict (like JSON)
    word_dict = word.model_dump(exclude_none=True)
    
    # Verify key fields are present
    assert word_dict["id"] == "de:hallo:1"
    assert word_dict["lemma"] == "Hallo"
    assert word_dict["lang"] == "de"
    assert word_dict["pos"] == "interjection"
    assert word_dict["defs"] == ["hello", "hi"]
    assert "examples" in word_dict
    assert word_dict["examples"][0]["text"] == "Hallo Welt!"
    assert word_dict["examples"][0]["tr"] == "Hello world!"


def test_word_with_learning_fields():
    """Test word with spaced repetition learning fields"""
    
    from datetime import timedelta
    
    now = datetime.now()
    future = now + timedelta(days=1)  # Next day instead of hour overflow
    
    word = Word(
        lemma="lernen",
        lang="de",
        pos=PartOfSpeech.VERB,
        defs=["to learn", "to study"],
        success_streak=5,
        last_reviewed_at=now,
        next_review_at=future,
        cefr=CEFRLevel.A2
    )
    
    assert word.success_streak == 5
    assert word.last_reviewed_at == now
    assert word.next_review_at == future
    assert word.cefr == CEFRLevel.A2