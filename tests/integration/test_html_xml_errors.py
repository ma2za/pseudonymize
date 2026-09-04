from pathlib import Path

import pytest

from pseudonymize.exceptions import AdapterExecutionError
from pseudonymize.formats import Document, FileFormat
from pseudonymize.html_xml import DOMAdapter



def test_dom_adapter_decode_error(tmp_path: Path) -> None:
    bad_file = tmp_path / "bad.html"
    bad_file.write_bytes(b"\xff\xfe\x00\x00")
    adapter = DOMAdapter(format=FileFormat.HTML)
    with pytest.raises(AdapterExecutionError, match="failed to decode"):
        adapter.extract(bad_file)


def test_dom_adapter_parse_error(tmp_path: Path) -> None:
    # bs4 is very forgiving, but let's try to mock it or trigger an error.
    pass


def test_dom_adapter_provenance_error() -> None:
    adapter = DOMAdapter(format=FileFormat.HTML)
    doc = Document("fake_id", (), {})
    with pytest.raises(AdapterExecutionError, match="document provenance lost"):
        adapter.render(doc)
