import json
import subprocess
import sys
from pathlib import Path

from benchmarks.evaluate_quality import evaluate


def test_in_process_evaluation_records_reproducibility_inputs(tmp_path: Path) -> None:
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

    result = evaluate(
        num_samples=1,
        use_ml=False,
        strict_labels=True,
        file_path=corpus,
    )

    assert result["file"] == str(corpus)
    assert isinstance(result["file_sha256"], str)
    assert len(result["file_sha256"]) == 64
    assert result["samples"] == 1
    assert "package_commit" in result
    policy_config = result["policy_configuration"]
    assert isinstance(policy_config, dict)
    assert policy_config["strict_labels"] is True
    assert "EMAIL" in policy_config["entity_types"]
    assert result["counts"] == {
        "true_positives": 1,
        "false_positives": 0,
        "false_negatives": 0,
        "out_of_scope": 0,
    }
    assert result["per_entity"] == {
        "EMAIL": {"true_positives": 1, "false_positives": 0, "false_negatives": 0}
    }


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
    try:
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
            timeout=30,
        )
    except subprocess.TimeoutExpired as exc:
        msg = f"evaluate_quality.py timed out. stdout={exc.stdout!r}, stderr={exc.stderr!r}"
        raise AssertionError(msg) from exc

    assert completed.returncode == 0, f"STDOUT: {completed.stdout}\nSTDERR: {completed.stderr}"
    result = json.loads(output.read_text(encoding="utf-8"))

    assert result["file"] == str(corpus)
    assert isinstance(result["file_sha256"], str)
    assert len(result["file_sha256"]) == 64
    assert result["samples"] == 1
    assert "package_commit" in result
    policy_config = result["policy_configuration"]
    assert isinstance(policy_config, dict)
    assert policy_config["strict_labels"] is True
    assert "EMAIL" in policy_config["entity_types"]
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
    try:
        completed = subprocess.run(
            [sys.executable, "benchmarks/evaluate_quality.py", "--samples", "1"],
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
        )
    except subprocess.TimeoutExpired as exc:
        msg = f"evaluate_quality.py timed out. stdout={exc.stdout!r}, stderr={exc.stderr!r}"
        raise AssertionError(msg) from exc

    assert completed.returncode == 2
    assert "--dataset-revision is required" in completed.stderr
