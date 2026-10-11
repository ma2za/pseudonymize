"""Execute the README quickstart against the installed library."""

import re
from pathlib import Path
from typing import Any

import pytest


def test_readme_python_examples(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    readme = Path(__file__).resolve().parents[2] / "README.md"
    examples = re.findall(r"^```python\n(.*?)^```", readme.read_text(encoding="utf-8"), re.M | re.S)
    assert examples, "README must contain executable Python examples"
    monkeypatch.chdir(tmp_path)
    (tmp_path / "requests.json").write_text('{"email": "reader@example.com"}', encoding="utf-8")
    namespace: dict[str, Any] = {}
    for index, example in enumerate(examples, start=1):
        exec(compile(example, f"README.md:python-example-{index}", "exec"), namespace)  # noqa: S102
    assert "reader@example.com" not in (tmp_path / "requests.safe.json").read_text(encoding="utf-8")
