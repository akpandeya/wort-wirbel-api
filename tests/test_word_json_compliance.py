"""
End-to-end test demonstrating JSON serialization matching issue #33 spec
"""

import json
from datetime import datetime
from app.domain.models import Word, PartOfSpeech, CEFRLevel, Example


def test_word_json_serialization_matches_spec():
    """Test that Word can be serialized to match the JSON format from issue #33"""
    
    # Create the word from the specification example
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
    
    # Serialize to dict (equivalent to JSON)
    word_dict = word.model_dump(exclude_none=True)
    
    # Expected structure based on issue #33
    expected_keys = {
        "id", "lemma", "lang", "pos", "pos_specific", "defs", "synonyms", 
        "examples", "freq_rank", "cefr", "audio", "src", "updated_at"
    }
    
    # Verify all expected keys are present
    for key in expected_keys:
        assert key in word_dict, f"Missing key: {key}"
    
    # Verify structure matches specification
    assert word_dict["id"] == "de:hallo:1"
    assert word_dict["lemma"] == "Hallo"
    assert word_dict["lang"] == "de"
    assert word_dict["pos"] == "interjection"
    assert word_dict["pos_specific"] == "Interjektion"
    assert word_dict["defs"] == ["hello", "hi"]
    assert word_dict["synonyms"] == ["hi", "guten Tag"]
    assert len(word_dict["examples"]) == 1
    assert word_dict["examples"][0] == {"text": "Hallo Welt!", "tr": "Hello world!"}
    assert word_dict["freq_rank"] == 523
    assert word_dict["cefr"] == "A1"
    assert word_dict["audio"] == "https://cdn.example.com/audio/de/hallo.mp3"
    assert word_dict["src"] == "dict-api-v1"
    
    # Verify it can be converted to actual JSON
    json_str = json.dumps(word_dict, default=str)
    assert json_str is not None
    
    # Verify it can be parsed back
    parsed = json.loads(json_str)
    assert parsed["lemma"] == "Hallo"
    assert parsed["pos"] == "interjection"


def test_word_deserialization_from_spec_json():
    """Test that we can create a Word from the JSON structure in the spec"""
    
    # JSON structure from issue #33 (modified to match our schema)
    json_data = {
        "id": "de:hallo:1",
        "lemma": "Hallo",
        "lang": "de",
        "pos": "interjection",
        "pos_specific": "Interjektion",
        "defs": ["hello", "hi"],
        "synonyms": ["hi", "guten Tag"],
        "examples": [
            {"text": "Hallo Welt!", "tr": "Hello world!"}
        ],
        "freq_rank": 523,
        "cefr": "A1",
        "audio": "https://cdn.example.com/audio/de/hallo.mp3",
        "src": "dict-api-v1",
        "updated_at": "2025-09-01T12:44:00"
    }
    
    # Convert examples to Example objects
    examples = [Example(**ex) for ex in json_data.get("examples", [])]
    json_data["examples"] = examples
    
    # Create Word from JSON data
    word = Word(**json_data)
    
    # Verify the word was created correctly
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
    assert word.audio == "https://cdn.example.com/audio/de/hallo.mp3"
    assert word.src == "dict-api-v1"


def test_comprehensive_schema_coverage():
    """Test that our schema covers all requirements from issue #33"""
    
    # Test word with all possible fields
    word = Word(
        # Core identification
        id="en:house:xyz789",
        lemma="house",
        lang="en",
        
        # Part of speech
        pos=PartOfSpeech.NOUN,
        pos_specific="Common noun",
        
        # Definitions and synonyms
        defs=["a building for human habitation", "dwelling", "residence"],
        synonyms=["home", "dwelling", "residence", "abode"],
        
        # Examples
        examples=[
            Example(text="This is my house.", tr="Das ist mein Haus."),
            Example(text="The house is big.", tr="Das Haus ist groß.")
        ],
        
        # Difficulty and frequency
        freq_rank=150,
        cefr=CEFRLevel.A1,
        
        # Grammar (not applicable for English, but testing fields)
        gender=None,
        plural="houses",
        
        # Media and source
        audio="https://cdn.example.com/audio/en/house.mp3",
        src="cambridge-dict-v2",
        
        # Learning progress
        success_streak=3,
        last_reviewed_at=datetime.now(),
        next_review_at=datetime.now(),
        
        # Timestamps
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    # Verify all fields are accessible
    assert word.id == "en:house:xyz789"
    assert word.lemma == "house"
    assert word.lang == "en"
    assert word.pos == PartOfSpeech.NOUN
    assert word.pos_specific == "Common noun"
    assert len(word.defs) == 3
    assert len(word.synonyms) == 4
    assert len(word.examples) == 2
    assert word.freq_rank == 150
    assert word.cefr == CEFRLevel.A1
    assert word.gender is None
    assert word.plural == "houses"
    assert word.audio.endswith("house.mp3")
    assert word.src == "cambridge-dict-v2"
    assert word.success_streak == 3
    assert word.last_reviewed_at is not None
    assert word.next_review_at is not None
    assert word.created_at is not None
    assert word.updated_at is not None
    
    print("✅ All fields from issue #33 specification are covered!")