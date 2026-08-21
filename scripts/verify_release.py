import argparse
import email.parser
import os
import tarfile
import tomllib
import zipfile
from pathlib import Path

MAXIMUM_WHEEL_BYTES = 250 * 1024
EXPECTED_PROJECT_URLS = {
    "Changelog": "https://github.com/ma2za/pseudonymize/blob/main/CHANGELOG.md",
    "Documentation": "https://ma2za.github.io/pseudonymize/",
    "Homepage": "https://github.com/ma2za/pseudonymize",
    "Issues": "https://github.com/ma2za/pseudonymize/issues",
    "Repository": "https://github.com/ma2za/pseudonymize",
    "Security": "https://github.com/ma2za/pseudonymize/security/policy",
}
EXPECTED_PYTHON_CLASSIFIERS = {
    f"Programming Language :: Python :: {version}" for version in ("3.11", "3.12", "3.13", "3.14")
}
EXPECTED_DEVELOPMENT_CLASSIFIER = "Development Status :: 5 - Production/Stable"
REQUIRED_SDIST_FILES = frozenset(
    {
        "CHANGELOG.md",
        "LICENSE",
        "README.md",
        "ROADMAP.md",
        "VISION.md",
        "docs/compatibility.md",
        "docs/deployment.md",
        "docs/llm-gateways.md",
        "docs/architecture.md",
        "docs/migration-a2.md",
        "docs/migration-a3.md",
        "docs/releasing.md",
        "docs/releases/0.1.0a2.md",
        "docs/releases/0.1.0a3.md",
        "docs/releases/0.1.0b1.md",
        "docs/releases/0.1.0rc1.md",
        "docs/releases/0.1.0.md",
        "examples/llm_gateway.py",
        "pyproject.toml",
        "scripts/audit_install.py",
        "src/pseudonymize/py.typed",
        "tests/corpus/files.json",
    }
)


def project_version(project_file: Path) -> str:
    with project_file.open("rb") as stream:
        configuration = tomllib.load(stream)
    return str(configuration["project"]["version"])


def verify_tag(version: str, tag: str | None) -> None:
    if tag and tag.removeprefix("v") != version:
        raise ValueError(f"tag {tag!r} does not match project version {version!r}")


def verify_wheel(path: Path, version: str, project_root: Path) -> None:
    if path.stat().st_size >= MAXIMUM_WHEEL_BYTES:
        raise ValueError(f"wheel exceeds {MAXIMUM_WHEEL_BYTES} bytes")
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        metadata_names = [name for name in names if name.endswith(".dist-info/METADATA")]
        if len(metadata_names) != 1:
            raise ValueError("wheel must contain exactly one METADATA file")
        metadata = email.parser.Parser().parsestr(archive.read(metadata_names[0]).decode("utf-8"))
        if metadata["Name"] != "pseudonymize" or metadata["Version"] != version:
            raise ValueError("wheel name or version does not match pyproject.toml")
        if metadata["License-Expression"] != "Apache-2.0":
            raise ValueError("wheel licence expression is invalid")
        if metadata["Requires-Python"] != ">=3.11":
            raise ValueError("wheel Python requirement is invalid")
        requirements = metadata.get_all("Requires-Dist", failobj=[])
        if any("extra ==" not in req for req in requirements):
            raise ValueError("base wheel must not declare runtime dependencies")
        project_urls = dict(
            value.split(", ", 1) for value in metadata.get_all("Project-URL", failobj=[])
        )
        if project_urls != EXPECTED_PROJECT_URLS:
            raise ValueError("wheel project URLs are invalid")
        classifiers = set(metadata.get_all("Classifier", failobj=[]))
        if EXPECTED_DEVELOPMENT_CLASSIFIER not in classifiers:
            raise ValueError("wheel development-status classifier is invalid")
        if not EXPECTED_PYTHON_CLASSIFIERS.issubset(classifiers):
            raise ValueError("wheel Python classifiers are incomplete")
        expected_package_files = {
            source.relative_to(project_root / "src").as_posix()
            for source in (project_root / "src" / "pseudonymize").rglob("*")
            if source.is_file() and (source.suffix == ".py" or source.name == "py.typed")
        }
        packaged_files = {name for name in names if name.startswith("pseudonymize/")}
        if packaged_files != expected_package_files:
            raise ValueError("wheel package files do not match the source tree")
        entry_points = [name for name in names if name.endswith(".dist-info/entry_points.txt")]
        if len(entry_points) != 1 or "pseudonymize = pseudonymize.cli:main" not in archive.read(
            entry_points[0]
        ).decode("utf-8"):
            raise ValueError("wheel does not expose the pseudonymize console script")
        wheel_metadata = [name for name in names if name.endswith(".dist-info/WHEEL")]
        if len(wheel_metadata) != 1 or "Tag: py3-none-any" not in archive.read(
            wheel_metadata[0]
        ).decode("utf-8"):
            raise ValueError("wheel is not a universal Python 3 wheel")
        licences = [name for name in names if name.endswith(".dist-info/licenses/LICENSE")]
        if (
            len(licences) != 1
            or archive.read(licences[0]) != (project_root / "LICENSE").read_bytes()
        ):
            raise ValueError("wheel does not contain the project licence")


def verify_sdist(path: Path, version: str) -> None:
    expected_root = f"pseudonymize-{version}"
    with tarfile.open(path, "r:gz") as archive:
        names = {
            name.removeprefix(f"{expected_root}/")
            for name in archive.getnames()
            if name.startswith(f"{expected_root}/")
        }
    missing = REQUIRED_SDIST_FILES - names
    if missing:
        raise ValueError(f"source distribution is missing: {', '.join(sorted(missing))}")


def verify_release(project_root: Path, distribution_directory: Path, tag: str | None) -> None:
    version = project_version(project_root / "pyproject.toml")
    verify_tag(version, tag)
    wheels = tuple(distribution_directory.glob("*.whl"))
    source_distributions = tuple(distribution_directory.glob("*.tar.gz"))
    if len(wheels) != 1 or len(source_distributions) != 1:
        raise ValueError("dist must contain exactly one wheel and one .tar.gz source distribution")
    verify_wheel(wheels[0], version, project_root)
    verify_sdist(source_distributions[0], version)
    print(
        f"verified pseudonymize {version}: {wheels[0].stat().st_size} byte wheel, "
        "typed, dependency-free, complete sdist"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--dist", type=Path, default=Path("dist"))
    inferred_tag = (
        os.environ.get("GITHUB_REF_NAME") if os.environ.get("GITHUB_REF_TYPE") == "tag" else None
    )
    parser.add_argument("--tag", default=inferred_tag)
    parser.add_argument("--check-tag-only", action="store_true")
    arguments = parser.parse_args()
    if arguments.check_tag_only:
        version = project_version(arguments.project_root / "pyproject.toml")
        verify_tag(version, arguments.tag)
        print(f"verified tag for pseudonymize {version}")
        return 0
    verify_release(arguments.project_root, arguments.dist, arguments.tag)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
