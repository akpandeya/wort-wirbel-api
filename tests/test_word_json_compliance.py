import json
from datetime import datetime
from app.domain.models import Word, PartOfSpeech, CEFRLevel, Example


def test_word_json_serialization_matches_spec():
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
        updated_at=datetime.fromisoformat("2025-09-01T12:44:00"),
    )

    word_dict = word.model_dump(exclude_none=True)
    expected_keys = {
        "id",
        "lemma",
        "lang",
        "pos",
        "pos_specific",
        "defs",
        "synonyms",
        "examples",
        "freq_rank",
        "cefr",
        "audio",
        "src",
        "updated_at",
    }

    for key in expected_keys:
        assert key in word_dict, f"Missing key: {key}"

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

    json_str = json.dumps(word_dict, default=str)
    assert json_str is not None

    parsed = json.loads(json_str)
    assert parsed["lemma"] == "Hallo"
    assert parsed["pos"] == "interjection"


def test_word_deserialization_from_spec_json():
    json_data = {
        "id": "de:hallo:1",
        "lemma": "Hallo",
        "lang": "de",
        "pos": "interjection",
        "pos_specific": "Interjektion",
        "defs": ["hello", "hi"],
        "synonyms": ["hi", "guten Tag"],
        "examples": [{"text": "Hallo Welt!", "tr": "Hello world!"}],
        "freq_rank": 523,
        "cefr": "A1",
        "audio": "https://cdn.example.com/audio/de/hallo.mp3",
        "src": "dict-api-v1",
        "updated_at": "2025-09-01T12:44:00",
    }

    examples = [Example(**ex) for ex in json_data.get("examples", [])]
    json_data["examples"] = examples

    word = Word(**json_data)

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
    word = Word(
        id="en:house:xyz789",
        lemma="house",
        lang="en",
        pos=PartOfSpeech.NOUN,
        pos_specific="Common noun",
        defs=["a building for human habitation", "dwelling", "residence"],
        synonyms=["home", "dwelling", "residence", "abode"],
        examples=[
            Example(text="This is my house.", tr="Das ist mein Haus."),
            Example(text="The house is big.", tr="Das Haus ist groß."),
        ],
        freq_rank=150,
        cefr=CEFRLevel.A1,
        gender=None,
        plural="houses",
        audio="https://cdn.example.com/audio/en/house.mp3",
        src="cambridge-dict-v2",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

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
    assert word.created_at is not None
    assert word.updated_at is not None

    print("✅ All fields from issue #33 specification are covered!")
