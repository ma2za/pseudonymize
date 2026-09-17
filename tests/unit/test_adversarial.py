import pytest

from pseudonymize import Pseudonymizer, TransformationMode, Policy
from pseudonymize.result import EntityType


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
    result = engine.process(text)
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
