import importlib
import sys
from pathlib import Path
from unittest import mock

import pytest

from pseudonymize.document import Document
from pseudonymize.engine import Pseudonymizer
from pseudonymize.exceptions import (
    AdapterContractError,
    AdapterExecutionError,
    UnsupportedFormatError,
)
from pseudonymize.formats import BuiltinFileAdapter, FileFormat
from pseudonymize.inspection import office, pdf
from pseudonymize.inspection.office import OfficeInspectionAdapter
from pseudonymize.inspection.pdf import PDFInspectionAdapter


def test_pdf_adapter_missing_dependency() -> None:
    with mock.patch.dict(sys.modules, {"pdfminer.high_level": None, "pdfminer.layout": None}):
        importlib.reload(pdf)
        with pytest.raises(RuntimeError, match="requires the 'pdf' extra"):
            pdf.PDFInspectionAdapter()
    importlib.reload(pdf)


def test_office_adapter_missing_dependency() -> None:
    with mock.patch.dict(sys.modules, {"docx": None, "openpyxl": None, "pptx": None}):
        importlib.reload(office)
        with pytest.raises(RuntimeError, match="requires the 'office' extra"):
            office.OfficeInspectionAdapter("docx")
    importlib.reload(office)


def test_office_adapter_invalid_format() -> None:
    with pytest.raises(ValueError, match="Unsupported Office format"):
        OfficeInspectionAdapter("unknown")


def test_pdf_adapter_execution_error(tmp_path: Path) -> None:
    adapter = PDFInspectionAdapter()
    invalid_file = tmp_path / "invalid.pdf"
    invalid_file.write_bytes(b"not a pdf")
    with pytest.raises(AdapterExecutionError, match="failed while reading the PDF"):
        adapter.extract(invalid_file)


def test_office_adapter_execution_error(tmp_path: Path) -> None:
    invalid_file = tmp_path / "invalid.docx"
    invalid_file.write_bytes(b"not a docx")
    with pytest.raises(AdapterExecutionError, match="failed while reading the DOCX"):
        OfficeInspectionAdapter("docx").extract(invalid_file)


@pytest.mark.parametrize(
    ("suffix", "adapter_factory"),
    [
        ("pdf", PDFInspectionAdapter),
        ("docx", lambda: OfficeInspectionAdapter("docx")),
    ],
)
def test_adapter_errors_expose_neither_path_nor_content(
    tmp_path: Path, suffix: str, adapter_factory: object
) -> None:
    directory = tmp_path / "acme-holdings"
    directory.mkdir()
    invalid_file = directory / f"payroll.{suffix}"
    invalid_file.write_bytes(b"not a document, mentions secret@example.com")
    adapter = adapter_factory()  # type: ignore[operator]
    with pytest.raises(AdapterExecutionError) as failure:
        adapter.extract(invalid_file)
    reported = str(failure.value)
    assert "acme-holdings" not in reported
    assert "payroll" not in reported
    assert "secret@example.com" not in reported
    # `from None` keeps the context object but suppresses it from tracebacks,
    # matching how the engine sanitizes adapter failures.
    assert failure.value.__cause__ is None
    assert failure.value.__suppress_context__


def test_pdf_adapter_render_contract() -> None:
    adapter = PDFInspectionAdapter()
    with pytest.raises(AdapterContractError, match="inspection only"):
        adapter.render(Document("test", (), {}))


def test_office_adapter_render_contract() -> None:
    adapter = OfficeInspectionAdapter("docx")
    with pytest.raises(AdapterContractError, match="inspection only"):
        adapter.render(Document("test", (), {}))


@pytest.mark.parametrize("suffix", [".pdf", ".docx", ".xlsx", ".pptx"])
def test_process_file_rejects_inspection_only_formats_before_reading(
    tmp_path: Path, suffix: str
) -> None:
    source = tmp_path / f"document{suffix}"
    source.write_bytes(b"never read")
    with pytest.raises(UnsupportedFormatError, match="inspection only"):
        Pseudonymizer().process_file(source, tmp_path / f"output{suffix}")
    assert not (tmp_path / f"output{suffix}").exists()


@pytest.mark.parametrize("format", ["pdf", "docx", "xlsx", "pptx"])
def test_builtin_adapter_rejects_inspection_only_formats(format: str) -> None:
    with pytest.raises(UnsupportedFormatError, match="text-based formats only"):
        BuiltinFileAdapter(FileFormat(format))


def test_inspect_file_rejects_encoding_for_inspection_only_formats(tmp_path: Path) -> None:
    source = tmp_path / "document.pdf"
    source.write_bytes(b"never read")
    with pytest.raises(ValueError, match="text-based formats"):
        Pseudonymizer().inspect_file(source, encoding="utf-8")
