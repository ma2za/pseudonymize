import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

DOCUMENTED_EXTRAS = ("html", "ml", "ocr", "office", "pdf", "remote")


def audit_extras(wheel_path: Path, python_executable: str | None = None) -> None:
    base_python = python_executable or sys.executable
    project_root = Path(__file__).resolve().parent.parent
    uv_bin = shutil.which("uv")
    if not uv_bin:
        raise RuntimeError("uv executable not found on PATH")

    with tempfile.TemporaryDirectory() as temporary_directory:
        for extra in DOCUMENTED_EXTRAS:
            extra_venv = Path(temporary_directory) / f"venv_{extra}"
            subprocess.run(  # noqa: S603
                [uv_bin, "venv", "--python", base_python, str(extra_venv)],
                check=True,
                capture_output=True,
            )
            extra_python = extra_venv / ("Scripts/python.exe" if os.name == "nt" else "bin/python")

            target = f"{wheel_path}[{extra}]"
            install_result = subprocess.run(  # noqa: S603
                [uv_bin, "pip", "install", "--python", str(extra_python), target],
                capture_output=True,
                text=True,
                check=False,
            )
            if install_result.returncode != 0:
                raise RuntimeError(f"failed to install extra {extra!r}: {install_result.stderr}")

            check_result = subprocess.run(  # noqa: S603
                [uv_bin, "pip", "check", "--python", str(extra_python)],
                capture_output=True,
                text=True,
                check=False,
            )
            if check_result.returncode != 0:
                raise RuntimeError(
                    f"dependency check failed for extra {extra!r}: {check_result.stderr}"
                )

            audit_script = project_root / "scripts" / "audit_install.py"
            audit_result = subprocess.run(  # noqa: S603
                [str(extra_python), "-I", str(audit_script), "--extra", extra],
                capture_output=True,
                text=True,
                check=False,
            )
            if audit_result.returncode != 0:
                raise RuntimeError(f"audit failed for extra {extra!r}: {audit_result.stderr}")
            print(f"verified clean isolated extra {extra}: {audit_result.stdout.strip()}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit clean isolated installation of every documented wheel extra."
    )
    parser.add_argument(
        "--dist",
        type=Path,
        default=Path("dist"),
        help="Path to directory containing built wheels (default: dist)",
    )
    parser.add_argument(
        "--python",
        type=str,
        default=None,
        help="Python version or executable to use for virtual environments",
    )
    arguments = parser.parse_args()

    wheels = tuple(arguments.dist.glob("*.whl"))
    if len(wheels) != 1:
        raise ValueError(f"expected exactly 1 wheel in {arguments.dist}, found {len(wheels)}")

    audit_extras(wheels[0], arguments.python)
    print("all documented extras verified in clean isolated environments")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
