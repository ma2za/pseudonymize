import json
from pathlib import Path

import pytest
from benchmarks.evaluate_external import (
    evaluate_external,
    extract_spans_from_row,
    load_local_jsonl,
)


def test_extract_spans_from_row_format_a() -> None:
    row = {
        "source_text": "Call me at +1-555-0199 or email user@test.com.",
        "privacy_mask": [
            {"start": 11, "end": 22, "label": "PHONE"},
            {"start": 32, "end": 45, "label": "EMAIL"},
        ],
    }
    text, spans = extract_spans_from_row(row)
    assert text == "Call me at +1-555-0199 or email user@test.com."
    assert spans == [(11, 22), (32, 45)]


def test_extract_spans_from_row_format_b() -> None:
    row = {
        "text": "Secret key: ABCD-1234-EFGH-5678",
        "spans": [{"start": 12, "end": 31, "label": "SECRET"}],
    }
    text, spans = extract_spans_from_row(row)
    assert text == "Secret key: ABCD-1234-EFGH-5678"
    assert spans == [(12, 31)]


def test_extract_spans_from_row_format_c_tokens() -> None:
    row = {
        "tokens": ["Contact", "alice@example.com", "now"],
        "ner_tags": [0, 1, 0],
    }
    text, spans = extract_spans_from_row(row)
    assert text == "Contact alice@example.com now"
    assert spans == [(8, 25)]


def test_extract_spans_from_row_invalid() -> None:
    with pytest.raises(ValueError, match="Unsupported row schema"):
        extract_spans_from_row({"invalid_key": "data"})


def test_load_local_jsonl(tmp_path: Path) -> None:
    file = tmp_path / "test.jsonl"
    file.write_text('{"text": "hello"}\n\n{"text": "world"}\n', encoding="utf-8")
    loaded = load_local_jsonl(file)
    assert len(loaded) == 2
    assert loaded[0]["text"] == "hello"
    assert loaded[1]["text"] == "world"


def test_evaluate_external_on_local_file(tmp_path: Path) -> None:
    corpus = tmp_path / "external_corpus.jsonl"
    corpus.write_text(
        json.dumps(
            {
                "source": "unit_test_source",
                "source_text": "Contact alice@example.com or visit https://example.com/login.",
                "privacy_mask": [
                    {"start": 8, "end": 25, "label": "EMAIL"},
                ],
            }
        )
        + "\n",
        encoding="utf-8",
    )

    res = evaluate_external(
        file_path=corpus,
        samples=1,
        use_ml=False,
    )

    assert res["benchmark"] == "external_generalization_track"
    assert res["samples"] == 1
    assert "character_micro_metrics" in res
    assert "character_macro_metrics" in res
    assert "sources" in res
    assert "unit_test_source" in res["sources"]

    source_stat = res["sources"]["unit_test_source"]
    assert source_stat["documents"] == 1
    assert source_stat["true_chars"] == 17
    # Email was detected by rule detector
    assert source_stat["masked_chars"] == 17
    assert source_stat["micro_recall"] == 1.0


def test_evaluate_external_adversarial_empty_spans(tmp_path: Path) -> None:
    corpus = tmp_path / "empty_corpus.jsonl"
    corpus.write_text(
        json.dumps(
            {
                "source": "clean_text",
                "source_text": "This is completely harmless and clean text with no PII.",
                "privacy_mask": [],
            }
        )
        + "\n",
        encoding="utf-8",
    )

    res = evaluate_external(
        file_path=corpus,
        samples=1,
        use_ml=False,
    )

    assert res["samples"] == 1
    micro = res["character_micro_metrics"]
    assert micro["true_chars"] == 0
    assert micro["masked_chars"] == 0
    assert micro["recall"] == 0.0
