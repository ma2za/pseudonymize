import json
import subprocess
import sys
from pathlib import Path


def test_local_evaluation_records_reproducibility_inputs(tmp_path: Path) -> None:
    corpus = tmp_path / "corpus.jsonl"
    corpus.write_text(
        json.dumps(
            {
                "language": "en",
                "source_text": "Email a@b.co",
                "privacy_mask": [{"start": 6, "end": 12, "label": "EMAIL"}],
            }
        )
        + "\n",
        encoding="utf-8",
    )

    output = tmp_path / "result.json"
    completed = subprocess.run(  # noqa: S603
        [
            sys.executable,
            "benchmarks/evaluate_quality.py",
            "--file",
            str(corpus),
            "--samples",
            "1",
            "--output",
            str(output),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr
    result = json.loads(output.read_text(encoding="utf-8"))

    assert result["file"] == str(corpus)
    assert isinstance(result["file_sha256"], str)
    assert len(result["file_sha256"]) == 64
    assert result["samples"] == 1
    assert "package_commit" in result
    assert "policy_configuration" in result
    assert result["policy_configuration"]["strict_labels"] is True
    assert "EMAIL" in result["policy_configuration"]["entity_types"]
    assert result["counts"] == {
        "true_positives": 1,
        "false_positives": 0,
        "false_negatives": 0,
        "out_of_scope": 0,
    }
    assert result["per_entity"] == {
        "EMAIL": {"true_positives": 1, "false_positives": 0, "false_negatives": 0}
    }


def test_remote_evaluation_requires_an_immutable_revision() -> None:
    completed = subprocess.run(
        [sys.executable, "benchmarks/evaluate_quality.py", "--samples", "1"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 2
    assert "--dataset-revision is required" in completed.stderr
