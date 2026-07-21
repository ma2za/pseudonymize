import argparse
import email.parser
import os
import tarfile
import tomllib
import zipfile
from pathlib import Path

MAXIMUM_WHEEL_BYTES = 250 * 1024
REQUIRED_SDIST_FILES = frozenset(
    {
        "LICENSE",
        "README.md",
        "ROADMAP.md",
        "VISION.md",
        "docs/architecture.md",
        "docs/releasing.md",
        "pyproject.toml",
        "src/pseudonymize/py.typed",
    }
)


def project_version(project_file: Path) -> str:
    with project_file.open("rb") as stream:
        configuration = tomllib.load(stream)
    return str(configuration["project"]["version"])


def verify_tag(version: str, tag: str | None) -> None:
    if tag and tag.removeprefix("v") != version:
        raise ValueError(f"tag {tag!r} does not match project version {version!r}")


def verify_wheel(path: Path, version: str) -> None:
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
        if metadata.get_all("Requires-Dist"):
            raise ValueError("base wheel must not declare runtime dependencies")
        if "pseudonymize/py.typed" not in names:
            raise ValueError("wheel does not contain pseudonymize/py.typed")
        entry_points = [name for name in names if name.endswith(".dist-info/entry_points.txt")]
        if len(entry_points) != 1 or "pseudonymize = pseudonymize.cli:main" not in archive.read(
            entry_points[0]
        ).decode("utf-8"):
            raise ValueError("wheel does not expose the pseudonymize console script")


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
    verify_wheel(wheels[0], version)
    verify_sdist(source_distributions[0], version)
    print(
        f"verified pseudonymize {version}: {wheels[0].stat().st_size} byte wheel, "
        "typed, dependency-free, complete sdist"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--dist", type=Path, default=Path("dist"))
    parser.add_argument("--tag", default=os.environ.get("GITHUB_REF_NAME"))
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
