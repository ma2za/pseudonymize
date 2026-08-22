from math import inf, nan
from types import MappingProxyType
from typing import Any, cast

import pytest

from pseudonymize.document import (
    ContentBlock,
    CoordinateLocation,
    CSVCellLocation,
    Document,
    JSONPathLocation,
    StructuralLocation,
    TextOffsetLocation,
)


def test_content_and_document_copy_metadata_and_hide_source_values() -> None:
    block_metadata = {"language": "en"}
    document_metadata = {"format": "custom"}
    block = ContentBlock(
        "body",
        "maria@example.com",
        TextOffsetLocation(0, 17),
        block_metadata,
    )
    document = Document("request", (block,), document_metadata)
    block_metadata["language"] = "it"
    document_metadata["format"] = "changed"

    assert block.metadata == {"language": "en"}
    assert document.metadata == {"format": "custom"}
    assert isinstance(block.metadata, MappingProxyType)
    assert isinstance(document.metadata, MappingProxyType)
    assert "maria@example.com" not in repr(block)
    assert "maria@example.com" not in repr(document)
    assert "custom" not in repr(document)
    with pytest.raises(TypeError):
        block.metadata["language"] = "de"  # type: ignore[index]


def test_document_requires_non_empty_unique_block_ids() -> None:
    location = TextOffsetLocation(0, 1)
    with pytest.raises(ValueError, match="block id"):
        ContentBlock("", "x", location)
    with pytest.raises(ValueError, match="document id"):
        Document("", ())
    block = ContentBlock("same", "x", location)
    with pytest.raises(ValueError, match="unique"):
        Document("duplicate", (block, block))
    assert Document("empty", ()).blocks == ()


@pytest.mark.parametrize(
    "metadata",
    [
        {"": "value"},
        {1: "value"},
        {"nested": {}},
        {"nested": []},
        {"number": nan},
        {"number": inf},
    ],
)
def test_metadata_rejects_non_json_scalar_values(metadata: dict[Any, Any]) -> None:
    with pytest.raises((TypeError, ValueError)):
        ContentBlock("body", "text", TextOffsetLocation(0, 4), metadata)
    with pytest.raises(TypeError, match="mapping"):
        ContentBlock(
            "body",
            "text",
            TextOffsetLocation(0, 4),
            cast(Any, (("key", "value"),)),
        )


def test_location_values_are_immutable_and_validated() -> None:
    assert JSONPathLocation(cast(tuple[str | int, ...], ["messages", 0, "content"])).path == (
        "messages",
        0,
        "content",
    )
    assert CSVCellLocation(0, 0).row == 0
    assert CoordinateLocation(1, 0.0, 0.0, 10.0, 10.0).page == 1
    assert StructuralLocation(("section", 1)).path == ("section", 1)

    with pytest.raises((TypeError, ValueError)):
        TextOffsetLocation(cast(int, True), 1)
    with pytest.raises(ValueError):
        TextOffsetLocation(-1, 1)
    with pytest.raises(ValueError):
        TextOffsetLocation(2, 1)
    with pytest.raises(TypeError):
        JSONPathLocation(("messages", cast(Any, True)))
    with pytest.raises(ValueError):
        JSONPathLocation(("messages", -1))
    with pytest.raises((TypeError, ValueError)):
        CSVCellLocation(cast(int, False), 0)
    with pytest.raises(ValueError):
        CSVCellLocation(0, -1)

    with pytest.raises(ValueError):
        CoordinateLocation(-1, 0.0, 0.0, 1.0, 1.0)
    with pytest.raises(TypeError):
        CoordinateLocation(1, float("inf"), 0.0, 1.0, 1.0)
    with pytest.raises(ValueError):
        CoordinateLocation(1, 10.0, 10.0, 0.0, 0.0)

    with pytest.raises(TypeError):
        StructuralLocation(("doc", cast(Any, True)))
    with pytest.raises(ValueError):
        StructuralLocation(("doc", -1))


def test_content_block_rejects_invalid_text_location_and_document_blocks() -> None:
    with pytest.raises(TypeError, match="text"):
        ContentBlock("body", cast(str, 1), TextOffsetLocation(0, 1))
    with pytest.raises(TypeError, match="location"):
        ContentBlock("body", "x", cast(Any, object()))
    with pytest.raises(TypeError, match="ContentBlock"):
        Document("bad", cast(Any, ("not-a-block",)))
