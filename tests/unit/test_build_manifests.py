from pathlib import Path

from benchmarks.build_manifests import (
    compute_template,
    compute_template_hash,
    partition_groups,
    write_manifest,
)


def test_compute_template_replaces_spans() -> None:
    text = "Contact Alice at alice@example.com."
    masks = [
        {"start": 8, "end": 13, "label": "PERSON"},
        {"start": 17, "end": 34, "label": "EMAIL"},
    ]
    template = compute_template(text, masks)
    assert template == "Contact <PERSON> at <EMAIL>."


def test_compute_template_hash_is_whitespace_invariant() -> None:
    t1 = "Hello <PERSON>   at   <EMAIL>."
    t2 = "Hello <PERSON> at <EMAIL>."
    assert compute_template_hash(t1) == compute_template_hash(t2)


def test_partition_groups_prevents_near_duplicate_leakage() -> None:
    # 3 rows, 2 share template A, 1 has template B
    rows = [
        {
            "source_text": "Call Alice at the office",
            "privacy_mask": [{"start": 5, "end": 10, "label": "PERSON"}],
        },
        {
            "source_text": "Call Bob at the office",
            "privacy_mask": [{"start": 5, "end": 8, "label": "PERSON"}],
        },
        {
            "source_text": "Email charlie@corp.org directly",
            "privacy_mask": [{"start": 6, "end": 22, "label": "EMAIL"}],
        },
    ]

    import hashlib

    alice_hash = hashlib.sha256(str(rows[0]["source_text"]).encode("utf-8")).hexdigest()
    bob_hash = hashlib.sha256(str(rows[1]["source_text"]).encode("utf-8")).hexdigest()

    partitions, _group_counts = partition_groups(rows)

    # Both template A rows (Alice & Bob) must be in the exact same partition
    found_partition = None
    for split_name, hash_list in partitions.items():
        if alice_hash in hash_list:
            found_partition = split_name
            break

    assert found_partition is not None
    assert bob_hash in partitions[found_partition]
    # And neither can appear in the other partitions
    for split_name, hash_list in partitions.items():
        if split_name != found_partition:
            assert alice_hash not in hash_list
            assert bob_hash not in hash_list


def test_write_manifest_creates_valid_json(tmp_path: Path) -> None:
    row_hashes = ["hash1", "hash2", "hash1"]
    out_path = write_manifest(
        tmp_path,
        "development",
        row_hashes,
        group_count=2,
        dataset_name="test_dataset",
        dataset_revision="rev_001",
    )
    assert out_path.exists()
    import json

    data = json.loads(out_path.read_text(encoding="utf-8"))
    assert data["split_name"] == "development"
    assert data["template_groups"] == 2
    assert data["total_rows"] == 3
    # Hashes are unique and sorted
    assert data["row_hashes"] == ["hash1", "hash2"]
