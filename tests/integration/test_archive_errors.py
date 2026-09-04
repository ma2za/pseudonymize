import pytest
from pathlib import Path
from pseudonymize.archive import ArchiveAdapter
from pseudonymize.exceptions import AdapterExecutionError
from pseudonymize.formats import FileFormat


def test_archive_bad_zip(tmp_path: Path) -> None:
    bad_zip = tmp_path / "bad.zip"
    bad_zip.write_bytes(b"not a zip")
    adapter = ArchiveAdapter(format=FileFormat.ZIP)
    with pytest.raises(AdapterExecutionError, match="failed to extract zip archive"):
        adapter.extract(bad_zip)


def test_archive_bad_tar(tmp_path: Path) -> None:
    bad_tar = tmp_path / "bad.tar"
    bad_tar.write_bytes(b"not a tar")
    adapter = ArchiveAdapter(format=FileFormat.TAR)
    with pytest.raises(AdapterExecutionError, match="failed to extract tar archive"):
        adapter.extract(bad_tar)
