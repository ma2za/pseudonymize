import shutil
import tarfile
import zipfile
from pathlib import Path

from pseudonymize import Pseudonymizer, TransformationMode


def test_zip_processing(tmp_path: Path) -> None:
    engine = Pseudonymizer(mode=TransformationMode.NUMBERED)

    in_dir = tmp_path / "in"
    in_dir.mkdir()

    (in_dir / "test.txt").write_text("Hello paolo@example.com", encoding="utf-8")
    (in_dir / "test.json").write_text('{"email": "secret@example.com"}', encoding="utf-8")
    (in_dir / "unsupported.bin").write_bytes(b"\x00\x01\x02")

    zip_path = tmp_path / "test.zip"
    shutil.make_archive(str(zip_path.with_suffix("")), "zip", in_dir)

    out_path = tmp_path / "out.zip"
    engine.process_file(zip_path, out_path)

    # Check output
    assert out_path.exists()

    out_dir = tmp_path / "out_unzip"
    shutil.unpack_archive(str(out_path), extract_dir=out_dir, format="zip")

    assert (out_dir / "test.txt").exists()
    txt = (out_dir / "test.txt").read_text(encoding="utf-8")
    assert "<EMAIL_1>" in txt or "<EMAIL_2>" in txt
    assert "paolo@example.com" not in txt

    assert (out_dir / "test.json").exists()
    js = (out_dir / "test.json").read_text(encoding="utf-8")
    assert "<EMAIL_1>" in js or "<EMAIL_2>" in js
    assert "secret@example.com" not in js

    assert (out_dir / "unsupported.bin").read_bytes() == b"\x00\x01\x02"


def test_tar_gz_processing(tmp_path: Path) -> None:
    engine = Pseudonymizer(mode=TransformationMode.NUMBERED)

    in_dir = tmp_path / "in"
    in_dir.mkdir()

    (in_dir / "test.md").write_text("Contact: paolo@example.com", encoding="utf-8")

    tar_path = tmp_path / "test.tar.gz"
    with tarfile.open(tar_path, "w:gz") as tar:
        tar.add(in_dir / "test.md", arcname="test.md")

    out_path = tmp_path / "out.tar.gz"
    engine.process_file(tar_path, out_path)

    assert out_path.exists()

    out_dir = tmp_path / "out_untar"
    out_dir.mkdir()

    # Secure extraction check
    if hasattr(tarfile, "data_filter"):
        with tarfile.open(out_path, "r:gz") as tar:
            tar.extractall(path=out_dir, filter="data")
    else:
        with tarfile.open(out_path, "r:gz") as tar:
            tar.extractall(path=out_dir)

    txt = (out_dir / "test.md").read_text(encoding="utf-8")
    assert "<EMAIL_1>" in txt
    assert "paolo@example.com" not in txt


def test_zipslip_prevention(tmp_path: Path) -> None:
    engine = Pseudonymizer()
    zip_path = tmp_path / "malicious.zip"

    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr(
            "../../../../../../../../../../../../../../../../../../../../tmp/evil.txt", "evil"
        )

    out_path = tmp_path / "safe.zip"
    engine.process_file(zip_path, out_path)

    # Should skip the malicious file
    with zipfile.ZipFile(out_path, "r") as zf:
        assert len(zf.namelist()) == 0
