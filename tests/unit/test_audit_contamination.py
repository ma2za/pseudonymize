import json
from pathlib import Path

from benchmarks.audit_contamination import audit_partitions


def test_audit_partitions_reports_clean_when_disjoint(tmp_path: Path) -> None:
    p_dev = tmp_path / "development_manifest.json"
    p_cal = tmp_path / "calibration_manifest.json"
    p_dev.write_text(json.dumps({"row_hashes": ["hash_1", "hash_2"]}))
    p_cal.write_text(json.dumps({"row_hashes": ["hash_3", "hash_4"]}))

    report = audit_partitions({"dev": p_dev, "cal": p_cal})
    assert report["clean_partitioning"] is True
    assert report["row_collisions"]["dev_vs_cal"] == 0


def test_audit_partitions_flags_overlap(tmp_path: Path) -> None:
    p_dev = tmp_path / "development_manifest.json"
    p_cal = tmp_path / "calibration_manifest.json"
    p_dev.write_text(json.dumps({"row_hashes": ["shared_hash", "hash_2"]}))
    p_cal.write_text(json.dumps({"row_hashes": ["shared_hash", "hash_4"]}))

    report = audit_partitions({"dev": p_dev, "cal": p_cal})
    assert report["clean_partitioning"] is False
    assert report["row_collisions"]["dev_vs_cal"] == 1
