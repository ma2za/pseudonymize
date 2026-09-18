from typing import Any

from pseudonymize import Pseudonymizer, TransformationMode


def test_subword_fragmentation_repair_trigger() -> None:
    # This tests the token-merge averaging repair heuristic
    engine = Pseudonymizer(mode=TransformationMode.REDACTED)

    # We create a weirdly spaced name that forces WordPiece to fragment
    text = "Please contact J o h n a t h a n  S m i t h s o n today."

    # Run it through the engine
    # Currently, we just want to ensure it doesnt crash or raise indexing errors
    # with the newly added character alignment.
    result = engine.process(text)
    assert result is not None


def test_extremely_long_overlapping_heuristics() -> None:
    # Repeated, overlapping triggers
    text = "mr mr mr mr mr mr mr mr mr mr mr mr dr dr dr dr dr dr dr ceo ceo ceo ceo ceo John Doe"
    engine = Pseudonymizer(mode=TransformationMode.REDACTED)
    result = engine.process(text)
    # The heuristic boosting logic should handle this without exponential blowup
    assert result is not None


def test_zero_gap_boundary_coercion() -> None:
    # Entities jammed against punctuation
    text = "Email:john.smith@example.com,Phone:+1-555-555-5555,Name:JohnSmith"
    engine = Pseudonymizer(mode=TransformationMode.REDACTED)
    result = engine.process(text)

    assert "john.smith@example.com" not in result.text
    assert "+1-555-555-5555" not in result.text
    # "JohnSmith" might or might not be detected depending on the model,
    # but the engine must safely align boundaries.


def test_lru_cache_bypassing_speed() -> None:
    # A single token repeated thousands of times should heavily trigger the LRU cache
    token = "London "
    text = token * 5000
    engine = Pseudonymizer(mode=TransformationMode.REDACTED)

    import time

    start = time.perf_counter()
    engine.process(text)
    end = time.perf_counter()

    # Cache hit should make this virtually instant vs raw ONNX inference
    # Just asserting it finishes without crashing
    assert end - start < 10.0  # Safe upper bound


def test_trailing_punctuation_in_context() -> None:
    # Triggers with weird punctuation
    text = "Visit city of:.,.#! Paris"
    engine = Pseudonymizer(mode=TransformationMode.REDACTED)
    result = engine.process(text)
    assert result is not None


def test_character_alignment_utf8_multi_byte() -> None:
    # Emoji and multi-byte characters near an entity boundary
    text = "Hello 🌍! My email is user@example.com."
    engine = Pseudonymizer(mode=TransformationMode.REDACTED)
    result = engine.process(text)
    assert "user@example.com" not in result.text
    assert "🌍" in result.text


def test_deeply_nested_json_adversarial() -> None:
    engine = Pseudonymizer(mode=TransformationMode.REDACTED)
    data: dict[str, Any] = {"a": "bob@example.com"}
    for _ in range(50):
        data = {"next": data}
    result = engine.process_data(data)
    assert str(result).find("bob@example.com") == -1


def test_adversarial_context_truncation() -> None:
    engine = Pseudonymizer(mode=TransformationMode.REDACTED)
    text = " ".join(["word"] * 400) + " Visit city of Paris"
    result = engine.process(text)
    assert result is not None


def test_adversarial_zero_width_chars_in_structured() -> None:
    engine = Pseudonymizer(mode=TransformationMode.REDACTED)
    text = "Call me at +1-​555‌-‍5555 for details."
    result = engine.process(text)
    assert result is not None


def test_adversarial_mixed_encodings() -> None:
    engine = Pseudonymizer(mode=TransformationMode.REDACTED)
    text = "My email is test@exаmple.com (with Cyrillic a)"  # noqa: RUF001
    result = engine.process(text)
    assert result is not None


def test_adversarial_newline_injections() -> None:
    engine = Pseudonymizer(mode=TransformationMode.REDACTED)
    text = "Visit\ncity\nof\nParis"
    result = engine.process(text)
    assert result is not None


def test_adversarial_trailing_surrogates() -> None:
    engine = Pseudonymizer(mode=TransformationMode.REDACTED)
    text = "Test email@example.com \ud83d"
    result = engine.process(text)
    assert result is not None


def test_adversarial_sql_injection_payloads() -> None:
    engine = Pseudonymizer(mode=TransformationMode.REDACTED)
    text = "SELECT * FROM users WHERE email = 'admin@example.com' OR name = 'DROP TABLE users'"
    result = engine.process(text)
    # The boundary regex logic might struggle with Chinese chars without word boundaries.
    # Just ensuring it survives without crashing.
    assert result is not None


def test_adversarial_base64_embedded() -> None:
    engine = Pseudonymizer(mode=TransformationMode.REDACTED)
    b64 = "A" * 1000 + "="
    text = "User: alice@example.com Token: " + b64
    result = engine.process(text)
    assert "alice@example.com" not in result.text


def test_adversarial_xml_entities() -> None:
    engine = Pseudonymizer(mode=TransformationMode.REDACTED)
    text = "Email: bob&#64;example.com"
    result = engine.process(text)
    assert result is not None


def test_adversarial_luhn_evasion() -> None:
    engine = Pseudonymizer(mode=TransformationMode.REDACTED)
    text = "Card: 4 5 3 2 - 1 1 1 1 - 2 2 2 2 - 3 3 3 4"
    result = engine.process(text)
    assert result is not None


def test_adversarial_pathological_overlap() -> None:
    engine = Pseudonymizer(mode=TransformationMode.REDACTED)
    text = "1234-5678-9012-3456"
    result = engine.process(text)
    assert result is not None


def test_adversarial_huge_number_of_entities() -> None:
    engine = Pseudonymizer(mode=TransformationMode.REDACTED)
    text = " ".join(["user" + str(i) + "@example.com" for i in range(500)])
    result = engine.process(text)
    assert "user10@example.com" not in result.text
    assert "user499@example.com" not in result.text


def test_adversarial_script_tag_injection() -> None:
    engine = Pseudonymizer(mode=TransformationMode.REDACTED)
    text = "<script>var email = 'hidden@example.com';</script>"
    result = engine.process(text)
    assert "hidden@example.com" not in result.text


def test_adversarial_recursive_acronyms() -> None:
    engine = Pseudonymizer(mode=TransformationMode.REDACTED)
    text = "CEO of FBI (Federal Bureau of Investigation) met with CIA."
    result = engine.process(text)
    assert result is not None


def test_adversarial_bidi_override() -> None:
    # Test Right-To-Left Override (U+202E) evasion technique
    engine = Pseudonymizer(mode=TransformationMode.REDACTED)
    # This renders as "moc.elpmaxe@bob" in standard editors, but contains bob@example.com backwards
    # RLO = ‮, PDF = ‬ (Pop Directional Formatting)
    text = "Email: ‮moc.elpmaxe@bob‬"
    result = engine.process(text)
    # The normalization logic should handle it or it should just survive without crashing
    assert result is not None


def test_adversarial_zalgo_text() -> None:
    # Test extreme combining characters over an identifier
    engine = Pseudonymizer(mode=TransformationMode.REDACTED)
    # "b" with multiple combining marks
    zalgo_email = "b̛̳̍̆͂̕o͆̾b̨̜̑@example.com"
    text = f"Contact {zalgo_email} immediately."
    result = engine.process(text)
    assert result is not None
    # Depending on unicode normalization (NFC/NFKC), it might catch it, but shouldn't crash.


def test_adversarial_massive_false_positives() -> None:
    # A text filled with thousands of common nouns that share names with LOC/PER
    engine = Pseudonymizer(mode=TransformationMode.REDACTED)
    # Words like "Hope", "Chase", "Hunter", "Forest", "Paris", "Washington"
    words = ["Hope", "Chase", "Hunter", "Forest", "Paris", "Washington", "Apple", "Mark"] * 200
    text = " ".join(words)
    result = engine.process(text)
    # Ensure this doesnt OOM or timeout the overlap resolver
    assert result is not None


def test_adversarial_markdown_links() -> None:
    # Test PII concealed inside markdown structures
    engine = Pseudonymizer(mode=TransformationMode.REDACTED)
    text = "Click [here](mailto:secret@example.com) to [visit 192.168.1.1](http://192.168.1.1)."
    result = engine.process(text)
    assert "secret@example.com" not in result.text
    assert "192.168.1.1" not in result.text


def test_adversarial_url_encoded_entities() -> None:
    # Test URL encoded identifiers
    engine = Pseudonymizer(mode=TransformationMode.REDACTED)
    text = "Target: %61%64%6D%69%6E%40%65%78%61%6D%70%6C%65%2E%63%6F%6D"
    result = engine.process(text)
    assert result is not None


def test_adversarial_multilingual_context_boundaries() -> None:
    # Test English PII surrounded directly by Chinese/Arabic characters without spacing
    engine = Pseudonymizer(mode=TransformationMode.REDACTED)
    text = "请联系admin@example.com谢谢"  # "Please contact admin@example.com thanks"
    result = engine.process(text)
    # The boundary regex logic might struggle with Chinese chars without word boundaries.
    # Just ensuring it survives without crashing.
    assert result is not None


def test_adversarial_unpaired_surrogates() -> None:
    # Test raw unpaired surrogate bytes that break strict UTF-8
    engine = Pseudonymizer(mode=TransformationMode.REDACTED)
    # \ud800 is a high surrogate with no low surrogate
    text = "Email: bob@example.com \ud800"
    result = engine.process(text)
    assert "bob@example.com" not in result.text


def test_adversarial_whitespace_injection() -> None:
    # Test tabs, vertical tabs, form feeds inside text
    engine = Pseudonymizer(mode=TransformationMode.REDACTED)
    text = "Email:\u0009\u000bbob@example.com\u000cPhone:\u0009555-555-5555"
    result = engine.process(text)
    assert "bob@example.com" not in result.text
