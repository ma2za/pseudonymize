from pathlib import Path
from typing import Any, cast

import pytest

from pseudonymize import ContentBlock, Document, Pseudonymizer, TextOffsetLocation
from pseudonymize.exceptions import (
    AdapterContractError,
    AdapterExecutionError,
    FileProcessingError,
)


class CustomInputAdapter:
    name = "custom-input"

    def extract(self, source: Path) -> Document:
        text = source.read_text(encoding="utf-8")
        return Document(
            "file",
            (ContentBlock("body", text, TextOffsetLocation(0, len(text))),),
            {"suffix": source.suffix},
        )


class CustomOutputAdapter:
    name = "custom-output"

    def render(self, document: Document) -> bytes:
        return document.blocks[0].text.encode("utf-8")


def test_generic_file_processing_uses_explicit_adapters_and_safe_destination(
    tmp_path: Path,
) -> None:
    source = tmp_path / "entrée.custom"
    source.write_text("Contact maria@example.com.", encoding="utf-8")

    result = Pseudonymizer().process_file(
        source,
        CustomInputAdapter(),
        CustomOutputAdapter(),
    )

    assert result.output == tmp_path / "entrée.safe.custom"
    assert result.output.read_text(encoding="utf-8") == "Contact <EMAIL_1>."
    assert source.read_text(encoding="utf-8") == "Contact maria@example.com."
    assert result.detections[0].block_id == "body"
    assert result.statistics.replacements_applied == 1
    assert not tuple(tmp_path.glob(".*.tmp"))


def test_destination_collision_requires_explicit_overwrite(tmp_path: Path) -> None:
    source = tmp_path / "input.payload"
    destination = tmp_path / "output.payload"
    source.write_text("maria@example.com", encoding="utf-8")
    destination.write_text("existing", encoding="utf-8")
    engine = Pseudonymizer()

    with pytest.raises(FileExistsError, match="already exists"):
        engine.process_file(
            source,
            CustomInputAdapter(),
            CustomOutputAdapter(),
            destination,
        )
    assert destination.read_text(encoding="utf-8") == "existing"

    result = engine.process_file(
        source,
        CustomInputAdapter(),
        CustomOutputAdapter(),
        destination,
        overwrite=True,
    )
    assert result.output == destination
    assert destination.read_text(encoding="utf-8") == "<EMAIL_1>"
    assert not tuple(tmp_path.glob(".*.tmp"))


def test_source_overwrite_is_always_forbidden(tmp_path: Path) -> None:
    source = tmp_path / "input.payload"
    source.write_text("maria@example.com", encoding="utf-8")

    with pytest.raises(ValueError, match="never overwrites"):
        Pseudonymizer().process_file(
            source,
            CustomInputAdapter(),
            CustomOutputAdapter(),
            source,
            overwrite=True,
        )
    assert source.read_text(encoding="utf-8") == "maria@example.com"


def test_source_symlink_cannot_bypass_overwrite_protection(tmp_path: Path) -> None:
    target = tmp_path / "target.payload"
    source = tmp_path / "alias.payload"
    target.write_text("maria@example.com", encoding="utf-8")
    try:
        source.symlink_to(target)
    except OSError:
        pytest.skip("symlinks are unavailable")

    with pytest.raises(ValueError, match="never overwrites"):
        Pseudonymizer().process_file(
            source,
            CustomInputAdapter(),
            CustomOutputAdapter(),
            target,
            overwrite=True,
        )
    assert target.read_text(encoding="utf-8") == "maria@example.com"


def test_inspect_file_does_not_create_output(tmp_path: Path) -> None:
    source = tmp_path / "input.custom"
    source.write_text("maria@example.com", encoding="utf-8")

    result = Pseudonymizer().inspect_file(source, CustomInputAdapter())

    assert result.output is None
    assert result.detections[0].token is None
    assert not (tmp_path / "input.safe.custom").exists()


def test_adapter_failures_are_sanitized_and_leave_no_temporary_file(
    tmp_path: Path,
) -> None:
    source_value = "maria@example.com"
    source = tmp_path / "input.custom"
    source.write_text(source_value, encoding="utf-8")

    class FailingInput:
        name = "failing-input"

        def extract(self, source: Path) -> Document:
            raise RuntimeError(source_value)

    with pytest.raises(AdapterExecutionError) as captured:
        Pseudonymizer().inspect_file(source, FailingInput())
    assert source_value not in str(captured.value)

    class FailingOutput:
        name = "failing-output"

        def render(self, document: Document) -> bytes:
            raise RuntimeError(source_value)

    with pytest.raises(AdapterExecutionError) as captured:
        Pseudonymizer().process_file(source, CustomInputAdapter(), FailingOutput())
    assert source_value not in str(captured.value)
    assert not tuple(tmp_path.glob(".*.tmp"))


def test_adapter_return_types_are_enforced(tmp_path: Path) -> None:
    source = tmp_path / "input.custom"
    source.write_text("maria@example.com", encoding="utf-8")

    class BadInput:
        name = "bad-input"

        def extract(self, source: Path) -> Document:
            return cast(Document, object())

    class BadOutput:
        name = "bad-output"

        def render(self, document: Document) -> bytes:
            return cast(bytes, "not-bytes")

    with pytest.raises(AdapterContractError, match="Document"):
        Pseudonymizer().inspect_file(source, BadInput())
    with pytest.raises(AdapterContractError, match="bytes"):
        Pseudonymizer().process_file(source, CustomInputAdapter(), BadOutput())


@pytest.mark.parametrize("function_name", ["link", "replace"])
def test_interrupted_atomic_publish_cleans_temporary_files(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    function_name: str,
) -> None:
    source = tmp_path / "input.custom"
    destination = tmp_path / "output.custom"
    source.write_text("maria@example.com", encoding="utf-8")
    if function_name == "replace":
        destination.write_text("existing", encoding="utf-8")

    def fail(*arguments: Any, **keywords: Any) -> None:
        raise OSError("maria@example.com")

    monkeypatch.setattr(f"pseudonymize.engine.os.{function_name}", fail)
    with pytest.raises(FileProcessingError) as captured:
        Pseudonymizer().process_file(
            source,
            CustomInputAdapter(),
            CustomOutputAdapter(),
            destination,
            overwrite=function_name == "replace",
        )

    assert "maria@example.com" not in str(captured.value)
    assert not tuple(tmp_path.glob(".*.tmp"))
    if function_name == "replace":
        assert destination.read_text(encoding="utf-8") == "existing"
    else:
        assert not destination.exists()


def test_atomic_no_clobber_handles_a_destination_race(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = tmp_path / "input.custom"
    destination = tmp_path / "output.custom"
    source.write_text("maria@example.com", encoding="utf-8")

    def collide(*arguments: Any, **keywords: Any) -> None:
        destination.write_text("racing writer", encoding="utf-8")
        raise FileExistsError

    monkeypatch.setattr("pseudonymize.engine.os.link", collide)
    with pytest.raises(FileExistsError, match="already exists"):
        Pseudonymizer().process_file(
            source,
            CustomInputAdapter(),
            CustomOutputAdapter(),
            destination,
        )
    assert destination.read_text(encoding="utf-8") == "racing writer"
    assert not tuple(tmp_path.glob(".*.tmp"))
