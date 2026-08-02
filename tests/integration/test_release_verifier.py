import email.message
import io
import tarfile
import zipfile
from pathlib import Path

import pytest
from scripts.verify_release import (
    EXPECTED_DEVELOPMENT_CLASSIFIER,
    EXPECTED_PROJECT_URLS,
    EXPECTED_PYTHON_CLASSIFIERS,
    REQUIRED_SDIST_FILES,
    project_version,
    verify_release,
    verify_tag,
)


def _write_project(root: Path, version: str = "0.1.0") -> None:
    (root / "pyproject.toml").write_text(
        f'[project]\nname = "pseudonymize"\nversion = "{version}"\n', encoding="utf-8"
    )
    (root / "LICENSE").write_text("licence", encoding="utf-8")
    package = root / "src" / "pseudonymize"
    package.mkdir(parents=True)
    (package / "py.typed").write_text("", encoding="utf-8")


def _write_wheel(
    directory: Path,
    version: str = "0.1.0",
    dependency: bool = False,
    development_classifier: str = EXPECTED_DEVELOPMENT_CLASSIFIER,
) -> None:
    metadata = email.message.Message()
    metadata["Name"] = "pseudonymize"
    metadata["Version"] = version
    metadata["License-Expression"] = "Apache-2.0"
    metadata["Requires-Python"] = ">=3.11"
    metadata["Classifier"] = development_classifier
    for label, url in EXPECTED_PROJECT_URLS.items():
        metadata["Project-URL"] = f"{label}, {url}"
    for classifier in EXPECTED_PYTHON_CLASSIFIERS:
        metadata["Classifier"] = classifier
    if dependency:
        metadata["Requires-Dist"] = "example"
    path = directory / f"pseudonymize-{version}-py3-none-any.whl"
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("pseudonymize/py.typed", "")
        archive.writestr(f"pseudonymize-{version}.dist-info/licenses/LICENSE", "licence")
        archive.writestr(f"pseudonymize-{version}.dist-info/METADATA", metadata.as_string())
        archive.writestr(
            f"pseudonymize-{version}.dist-info/WHEEL",
            "Wheel-Version: 1.0\nTag: py3-none-any\n",
        )
        archive.writestr(
            f"pseudonymize-{version}.dist-info/entry_points.txt",
            "[console_scripts]\npseudonymize = pseudonymize.cli:main\n",
        )


def _write_sdist(directory: Path, version: str = "0.1.0") -> None:
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
    verify_release(tmp_path, distribution_directory, "v0.1.0")
    assert "dependency-free" in capsys.readouterr().out
    assert project_version(tmp_path / "pyproject.toml") == "0.1.0"


def test_release_rejects_mismatched_tag() -> None:
    with pytest.raises(ValueError, match="does not match"):
        verify_tag("0.1.0", "v0.1.0rc1")


def test_release_rejects_runtime_dependency(tmp_path: Path) -> None:
    _write_project(tmp_path)
    distribution_directory = tmp_path / "dist"
    distribution_directory.mkdir()
    _write_wheel(distribution_directory, dependency=True)
    _write_sdist(distribution_directory)
    with pytest.raises(ValueError, match="runtime dependencies"):
        verify_release(tmp_path, distribution_directory, None)


def test_release_rejects_prerelease_classifier(tmp_path: Path) -> None:
    _write_project(tmp_path)
    distribution_directory = tmp_path / "dist"
    distribution_directory.mkdir()
    _write_wheel(
        distribution_directory,
        development_classifier="Development Status :: 4 - Beta",
    )
    _write_sdist(distribution_directory)
    with pytest.raises(ValueError, match="development-status classifier"):
        verify_release(tmp_path, distribution_directory, None)
