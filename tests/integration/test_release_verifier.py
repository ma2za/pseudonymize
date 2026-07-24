import email.message
import io
import tarfile
import zipfile
from pathlib import Path

import pytest
from scripts.verify_release import (
    REQUIRED_SDIST_FILES,
    project_version,
    verify_release,
    verify_tag,
)


def _write_project(root: Path, version: str = "0.1.0a3") -> None:
    (root / "pyproject.toml").write_text(
        f'[project]\nname = "pseudonymize"\nversion = "{version}"\n', encoding="utf-8"
    )


def _write_wheel(directory: Path, version: str = "0.1.0a3", dependency: bool = False) -> None:
    metadata = email.message.Message()
    metadata["Name"] = "pseudonymize"
    metadata["Version"] = version
    if dependency:
        metadata["Requires-Dist"] = "example"
    path = directory / f"pseudonymize-{version}-py3-none-any.whl"
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("pseudonymize/py.typed", "")
        archive.writestr(f"pseudonymize-{version}.dist-info/METADATA", metadata.as_string())
        archive.writestr(
            f"pseudonymize-{version}.dist-info/entry_points.txt",
            "[console_scripts]\npseudonymize = pseudonymize.cli:main\n",
        )


def _write_sdist(directory: Path, version: str = "0.1.0a3") -> None:
    path = directory / f"pseudonymize-{version}.tar.gz"
    with tarfile.open(path, "w:gz") as archive:
        for name in REQUIRED_SDIST_FILES:
            value = b"test"
            information = tarfile.TarInfo(f"pseudonymize-{version}/{name}")
            information.size = len(value)
            archive.addfile(information, io.BytesIO(value))


def test_release_artifacts_and_tag(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    _write_project(tmp_path)
    distribution_directory = tmp_path / "dist"
    distribution_directory.mkdir()
    _write_wheel(distribution_directory)
    _write_sdist(distribution_directory)
    verify_release(tmp_path, distribution_directory, "v0.1.0a3")
    assert "dependency-free" in capsys.readouterr().out
    assert project_version(tmp_path / "pyproject.toml") == "0.1.0a3"


def test_release_rejects_mismatched_tag() -> None:
    with pytest.raises(ValueError, match="does not match"):
        verify_tag("0.1.0a3", "v0.1.0a2")


def test_release_rejects_runtime_dependency(tmp_path: Path) -> None:
    _write_project(tmp_path)
    distribution_directory = tmp_path / "dist"
    distribution_directory.mkdir()
    _write_wheel(distribution_directory, dependency=True)
    _write_sdist(distribution_directory)
    with pytest.raises(ValueError, match="runtime dependencies"):
        verify_release(tmp_path, distribution_directory, None)
