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

    if hasattr(tarfile, "data_filter"):
        with tarfile.open(out_path, "r:gz") as tar:
            tar.extractall(path=out_dir, filter="data")
    else:
        with tarfile.open(out_path, "r:gz") as tar:
            tar.extractall(path=out_dir)

    txt = (out_dir / "test.md").read_text(encoding="utf-8")
    assert "<EMAIL_1>" in txt
    assert "paolo@example.com" not in txt


def test_deeply_nested_archive(tmp_path: Path) -> None:
    """Ensure that inner archives are handled recursively by the engine."""
    engine = Pseudonymizer(mode=TransformationMode.NUMBERED)

    # 1. Create inner tar.gz
    inner_dir = tmp_path / "inner"
    inner_dir.mkdir()
    (inner_dir / "secret.txt").write_text("My email is nested@example.com", encoding="utf-8")
    
    tar_path = tmp_path / "inner.tar.gz"
    with tarfile.open(tar_path, "w:gz") as tar:
        tar.add(inner_dir / "secret.txt", arcname="secret.txt")

    # 2. Wrap in outer zip
    zip_path = tmp_path / "outer.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.write(tar_path, "inner.tar.gz")

    out_path = tmp_path / "out.zip"
    engine.process_file(zip_path, out_path)

    assert out_path.exists()
    
    # 3. Verify
    out_dir = tmp_path / "out_unzip"
    shutil.unpack_archive(str(out_path), extract_dir=out_dir, format="zip")
    
    inner_out = out_dir / "inner.tar.gz"
    assert inner_out.exists()
    
    out_tar_dir = tmp_path / "out_untar"
    out_tar_dir.mkdir()
    with tarfile.open(inner_out, "r:gz") as tar:
        if hasattr(tarfile, "data_filter"):
            tar.extractall(path=out_tar_dir, filter="data")
        else:
            tar.extractall(path=out_tar_dir)
        
    txt = (out_tar_dir / "secret.txt").read_text(encoding="utf-8")
    assert "<EMAIL_1>" in txt
    assert "nested@example.com" not in txt


def test_zipslip_prevention(tmp_path: Path) -> None:
    engine = Pseudonymizer()
    zip_path = tmp_path / "malicious.zip"

    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr(
            "../../../../../../../../../../../../../../../../../../../../tmp/evil.txt", "evil"
        )
        zf.writestr(
            "/absolute/path/to/evil2.txt", "evil"
        )
        zf.writestr(
            "C:\\Windows\\System32\\evil3.txt", "evil"
        )
        zf.writestr(
            "safe_file.txt", "safe email@example.com"
        )

    out_path = tmp_path / "safe.zip"
    engine.process_file(zip_path, out_path)

    # Should skip the malicious files but keep the safe one
    with zipfile.ZipFile(out_path, "r") as zf:
        names = zf.namelist()
        assert len(names) == 1
        assert names[0] == "safe_file.txt"
        content = zf.read("safe_file.txt").decode("utf-8")
        assert "email@example.com" not in content

def test_tar_traversal_prevention(tmp_path: Path) -> None:
    engine = Pseudonymizer()
    tar_path = tmp_path / "malicious.tar"
    
    with tarfile.open(tar_path, "w") as tf:
        # Create a malicious tarinfo
        ti = tarfile.TarInfo(name="../../../evil.txt")
        ti.size = 4
        import io
        tf.addfile(ti, io.BytesIO(b"evil"))
        
        # Add a safe file
        safe_path = tmp_path / "safe.txt"
        safe_path.write_text("safe email@example.com")
        tf.add(safe_path, arcname="safe.txt")
        
    out_path = tmp_path / "safe.tar"
    engine.process_file(tar_path, out_path)
    
    with tarfile.open(out_path, "r") as tf:
        names = tf.getnames()
        assert len(names) == 1
        assert names[0] == "safe.txt"
