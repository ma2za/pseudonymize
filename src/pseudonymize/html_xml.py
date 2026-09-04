from pathlib import Path
from typing import Any

from bs4 import BeautifulSoup, NavigableString  # type: ignore[attr-defined]

from pseudonymize.document import ContentBlock, Document, JSONPathLocation
from pseudonymize.exceptions import AdapterExecutionError
from pseudonymize.formats import FileFormat


class DOMAdapter:
    def __init__(self, format: FileFormat, encoding: str | None = None) -> None:
        self.format = format
        self.encoding = encoding or "utf-8"
        self._parser = "xml" if format is FileFormat.XML else "html.parser"
        self._doc_map: dict[str, BeautifulSoup] = {}

    def extract(self, source: Path) -> Document:
        try:
            content = source.read_text(encoding=self.encoding)
        except UnicodeDecodeError as e:
            raise AdapterExecutionError(f"failed to decode {self.format.value}") from e

        try:
            soup = BeautifulSoup(content, self._parser)
        except Exception as e:
            raise AdapterExecutionError(f"failed to parse {self.format.value}") from e

        doc_id = str(source)
        self._doc_map[doc_id] = soup

        blocks: list[ContentBlock] = []

        def traverse(node: Any, path: tuple[str | int, ...]) -> None:
            if hasattr(node, "name") and node.name is not None:
                # E.g. skip script/style tags if needed, but for now we extract all text
                for i, child in enumerate(node.children):
                    traverse(child, (*path, node.name, i))

                # Check attributes for sensitive data like href or title
                if hasattr(node, "attrs") and node.attrs:
                    for k, v in node.attrs.items():
                        if isinstance(v, str):
                            loc_path = (*path, f"@{k}")
                            loc = JSONPathLocation(loc_path)
                            path_str = ".".join(str(p) for p in loc_path)
                            blocks.append(ContentBlock(f"{doc_id}:{path_str}", v, loc))
            elif isinstance(node, NavigableString):
                text = str(node).strip()
                if text:
                    loc = JSONPathLocation(path)
                    path_str = ".".join(str(p) for p in path)
                    blocks.append(ContentBlock(f"{doc_id}:{path_str}", str(node), loc))

        traverse(soup, ())
        return Document(doc_id, tuple(blocks), {"source_path": doc_id})

    def render(self, document: Document) -> bytes:
        doc_id = document.metadata.get("source_path")
        if not isinstance(doc_id, str) or doc_id not in self._doc_map:
            raise AdapterExecutionError("document provenance lost or invalid")

        soup = self._doc_map[doc_id]

        block_map = {b.id: b.text for b in document.blocks}

        def traverse_update(node: Any, path: tuple[str | int, ...]) -> None:
            if hasattr(node, "name") and node.name is not None:
                for i, child in enumerate(node.children):
                    traverse_update(child, (*path, node.name, i))
                if hasattr(node, "attrs") and node.attrs:
                    for k, v in list(node.attrs.items()):
                        if isinstance(v, str):
                            loc_path = (*path, f"@{k}")
                            path_str = ".".join(str(p) for p in loc_path)
                            ident = f"{doc_id}:{path_str}"
                            if ident in block_map:
                                node[k] = block_map[ident]
            elif isinstance(node, NavigableString):
                path_str = ".".join(str(p) for p in path)
                ident = f"{doc_id}:{path_str}"
                if ident in block_map:
                    node.replace_with(block_map[ident])

        traverse_update(soup, ())
        # We need to return exactly the type of encoding specified
        return str(soup).encode(self.encoding)
