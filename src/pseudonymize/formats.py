import codecs
import csv
import io
import json
import sys
import threading
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import TypeAlias, cast

from pseudonymize.document import (
    ContentBlock,
    CSVCellLocation,
    Document,
    JSONPathLocation,
    TextOffsetLocation,
)
from pseudonymize.exceptions import (
    AdapterContractError,
    AdapterExecutionError,
    UnsupportedFormatError,
)

JSONValue: TypeAlias = str | int | float | bool | dict[str, "JSONValue"] | list["JSONValue"] | None


class FileFormat(StrEnum):
    TEXT = "text"
    MARKDOWN = "markdown"
    LOG = "log"
    JSON = "json"
    JSONL = "jsonl"
    CSV = "csv"


_SUFFIX_FORMATS = {
    ".txt": FileFormat.TEXT,
    ".md": FileFormat.MARKDOWN,
    ".markdown": FileFormat.MARKDOWN,
    ".log": FileFormat.LOG,
    ".json": FileFormat.JSON,
    ".jsonl": FileFormat.JSONL,
    ".ndjson": FileFormat.JSONL,
    ".csv": FileFormat.CSV,
}
_CSV_LIMIT_LOCK = threading.Lock()


def select_file_format(path: Path, explicit: FileFormat | str | None) -> FileFormat:
    if explicit is not None:
        try:
            return FileFormat(explicit)
        except ValueError:
            raise UnsupportedFormatError("unsupported file format") from None
    selected = _SUFFIX_FORMATS.get(path.suffix.lower())
    if selected is None:
        raise UnsupportedFormatError("file format is unsupported; pass format explicitly")
    return selected


@dataclass(slots=True)
class BuiltinFileAdapter:
    format: FileFormat
    encoding: str | None = None
    _state: "_AdapterState | None" = field(default=None, init=False, repr=False)

    def extract(self, source: Path) -> Document:
        decoded = _decode(source.read_bytes(), self.encoding)
        content: object
        if self.format in {FileFormat.TEXT, FileFormat.MARKDOWN, FileFormat.LOG}:
            document, content = _extract_text(decoded.text, self.format, decoded)
        elif self.format is FileFormat.JSON:
            document, content = _extract_json(decoded.text, decoded)
        elif self.format is FileFormat.JSONL:
            try:
                document, content = _extract_jsonl(decoded.text, decoded)
            except _JSONLLineError as error:
                raise AdapterExecutionError(
                    f"input adapter failed at JSONL line {error.line}"
                ) from None
        else:
            document, content = _extract_csv(decoded.text, decoded)
        self._state = _AdapterState(document, content, decoded)
        return document

    def render(self, document: Document) -> bytes:
        state = self._state
        if state is None:
            raise AdapterContractError("built-in adapter must extract before rendering")
        _validate_document(document, state.document)
        if self.format in {FileFormat.TEXT, FileFormat.MARKDOWN, FileFormat.LOG}:
            text = _render_text(document)
        elif self.format is FileFormat.JSON:
            text = _render_json(document, state)
        elif self.format is FileFormat.JSONL:
            text = _render_jsonl(document, state)
        else:
            text = _render_csv(document, state)
        return _encode(text, state.decoded)


@dataclass(frozen=True, slots=True)
class _DecodedText:
    text: str = field(repr=False)
    encoding: str
    bom: bool


@dataclass(frozen=True, slots=True)
class _AdapterState:
    document: Document
    content: object = field(repr=False)
    decoded: _DecodedText


@dataclass(frozen=True, slots=True)
class _JSONLLineError(Exception):
    line: int


def _decode(data: bytes, encoding: str | None) -> _DecodedText:
    selected = encoding or "utf-8"
    normalized = codecs.lookup(selected).name
    bom = normalized == "utf-8" and data.startswith(codecs.BOM_UTF8)
    payload = data[len(codecs.BOM_UTF8) :] if bom else data
    return _DecodedText(payload.decode(selected, errors="strict"), normalized, bom)


def _encode(text: str, decoded: _DecodedText) -> bytes:
    data = text.encode(decoded.encoding, errors="strict")
    if decoded.bom:
        return codecs.BOM_UTF8 + data
    return data


def _metadata(format: FileFormat, decoded: _DecodedText) -> dict[str, str | bool]:
    return {
        "format": format.value,
        "encoding": decoded.encoding,
        "bom": decoded.bom,
    }


def _extract_text(text: str, format: FileFormat, decoded: _DecodedText) -> tuple[Document, str]:
    block = ContentBlock("body", text, TextOffsetLocation(0, len(text)))
    return Document("file", (block,), _metadata(format, decoded)), text


def _render_text(document: Document) -> str:
    return document.blocks[0].text


def _reject_duplicate_keys(pairs: list[tuple[str, JSONValue]]) -> dict[str, JSONValue]:
    result: dict[str, JSONValue] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("JSON object contains duplicate keys")
        result[key] = value
    return result


def _reject_constant(value: str) -> JSONValue:
    raise ValueError("JSON contains a non-finite number")


def _load_json(text: str) -> JSONValue:
    return cast(
        JSONValue,
        json.loads(
            text,
            object_pairs_hook=_reject_duplicate_keys,
            parse_constant=_reject_constant,
        ),
    )


def _string_blocks(
    value: JSONValue,
    path: tuple[str | int, ...],
    blocks: list[ContentBlock],
    *,
    prefix: str = "block",
) -> None:
    if isinstance(value, str):
        blocks.append(
            ContentBlock(
                f"{prefix}-{len(blocks):06d}",
                value,
                JSONPathLocation(path),
            )
        )
    elif isinstance(value, dict):
        for key, item in value.items():
            _string_blocks(item, (*path, key), blocks, prefix=prefix)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _string_blocks(item, (*path, index), blocks, prefix=prefix)


def _extract_json(text: str, decoded: _DecodedText) -> tuple[Document, JSONValue]:
    value = _load_json(text)
    blocks: list[ContentBlock] = []
    _string_blocks(value, (), blocks)
    return Document("file", tuple(blocks), _metadata(FileFormat.JSON, decoded)), value


def _replace_json_strings(
    value: JSONValue,
    path: tuple[str | int, ...],
    replacements: dict[tuple[str | int, ...], str],
) -> JSONValue:
    if isinstance(value, str):
        try:
            return replacements[path]
        except KeyError:
            raise AdapterContractError("JSON document structure changed") from None
    if isinstance(value, dict):
        return {
            key: _replace_json_strings(item, (*path, key), replacements)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [
            _replace_json_strings(item, (*path, index), replacements)
            for index, item in enumerate(value)
        ]
    return value


def _json_replacements(document: Document) -> dict[tuple[str | int, ...], str]:
    replacements: dict[tuple[str | int, ...], str] = {}
    for block in document.blocks:
        if not isinstance(block.location, JSONPathLocation):
            raise AdapterContractError("JSON document location changed")
        path = block.location.path
        if path in replacements:
            raise AdapterContractError("JSON document contains duplicate locations")
        replacements[path] = block.text
    return replacements


def _render_json(document: Document, state: _AdapterState) -> str:
    value = _replace_json_strings(
        _require_json_content(state.content),
        (),
        _json_replacements(document),
    )
    return json.dumps(value, ensure_ascii=False, allow_nan=False, indent=2) + "\n"


def _extract_jsonl(text: str, decoded: _DecodedText) -> tuple[Document, tuple[JSONValue, ...]]:
    if not text:
        values: tuple[JSONValue, ...] = ()
    else:
        lines = text.splitlines()
        values_list: list[JSONValue] = []
        blocks: list[ContentBlock] = []
        for line_index, line in enumerate(lines):
            if not line.strip():
                raise _JSONLLineError(line_index + 1)
            try:
                value = _load_json(line)
            except (TypeError, ValueError):
                raise _JSONLLineError(line_index + 1) from None
            values_list.append(value)
            _string_blocks(
                value,
                (line_index,),
                blocks,
                prefix=f"line-{line_index:06d}-block",
            )
        values = tuple(values_list)
        return (
            Document("file", tuple(blocks), _metadata(FileFormat.JSONL, decoded)),
            values,
        )
    return Document("file", (), _metadata(FileFormat.JSONL, decoded)), values


def _validate_document(document: Document, original: Document) -> None:
    if (
        document.id != original.id
        or document.metadata != original.metadata
        or tuple((block.id, block.location) for block in document.blocks)
        != tuple((block.id, block.location) for block in original.blocks)
    ):
        raise AdapterContractError("document structure changed")


def _render_jsonl(document: Document, state: _AdapterState) -> str:
    values = _require_jsonl_content(state.content)
    replacements = _json_replacements(document)
    rendered = (
        json.dumps(
            _replace_json_strings(value, (line_index,), replacements),
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
        )
        for line_index, value in enumerate(values)
    )
    return "".join(f"{line}\n" for line in rendered)


def _extract_csv(text: str, decoded: _DecodedText) -> tuple[Document, tuple[tuple[str, ...], ...]]:
    rows = _read_csv(text)
    blocks = tuple(
        ContentBlock(
            f"row-{row_index:06d}-column-{column_index:06d}",
            value,
            CSVCellLocation(row_index, column_index),
        )
        for row_index, row in enumerate(rows)
        for column_index, value in enumerate(row)
    )
    metadata = _metadata(FileFormat.CSV, decoded)
    metadata["dialect"] = "excel"
    return Document("file", blocks, metadata), rows


def _read_csv(text: str) -> tuple[tuple[str, ...], ...]:
    with _CSV_LIMIT_LOCK:
        previous_limit = csv.field_size_limit()
        try:
            csv.field_size_limit(sys.maxsize)
            return tuple(
                tuple(row) for row in csv.reader(io.StringIO(text, newline=""), strict=True)
            )
        finally:
            csv.field_size_limit(previous_limit)


def _render_csv(document: Document, state: _AdapterState) -> str:
    rows = _require_csv_content(state.content)
    replacements = {
        (
            cast(CSVCellLocation, block.location).row,
            cast(CSVCellLocation, block.location).column,
        ): block.text
        for block in document.blocks
    }
    transformed = [
        [replacements[(row_index, column_index)] for column_index in range(len(row))]
        for row_index, row in enumerate(rows)
    ]
    output = io.StringIO(newline="")
    csv.writer(output, dialect="excel", lineterminator="\r\n").writerows(transformed)
    return output.getvalue()


def _require_json_content(content: object) -> JSONValue:
    return cast(JSONValue, content)


def _require_jsonl_content(content: object) -> tuple[JSONValue, ...]:
    return cast(tuple[JSONValue, ...], content)


def _require_csv_content(content: object) -> tuple[tuple[str, ...], ...]:
    return cast(tuple[tuple[str, ...], ...], content)
