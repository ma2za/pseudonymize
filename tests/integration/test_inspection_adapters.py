from pathlib import Path

import pytest

from pseudonymize.engine import Pseudonymizer
from pseudonymize.formats import FileFormat
from pseudonymize.policy import Policy

# Optional imports for generators
try:
    import fpdf

    HAS_FPDF = True
except ImportError:
    HAS_FPDF = False

try:
    import docx
    import openpyxl
    import pptx

    HAS_OFFICE = True
except ImportError:
    HAS_OFFICE = False

pytestmark = pytest.mark.integration


@pytest.fixture
def test_pdf_path(tmp_path: Path) -> Path:
    if not HAS_FPDF:
        pytest.skip("fpdf2 not installed")
    path = tmp_path / "test.pdf"
    pdf = fpdf.FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", size=12)
    pdf.cell(text="Contact me at alice@example.com for more info.")
    pdf.ln()
    pdf.cell(text="   ")
    pdf.output(str(path))
    return path


@pytest.fixture
def test_docx_path(tmp_path: Path) -> Path:
    if not HAS_OFFICE:
        pytest.skip("python-docx not installed")
    path = tmp_path / "test.docx"
    doc = docx.Document()
    doc.add_paragraph("Hello, my email is bob@example.com.")
    doc.add_paragraph("   ")  # Empty text
    table = doc.add_table(rows=2, cols=2)
    table.rows[0].cells[0].text = "Header"
    table.rows[0].cells[1].text = "Value"
    table.rows[1].cells[0].text = "Data"
    table.rows[1].cells[1].text = "   "  # Empty text
    doc.save(str(path))
    return path


@pytest.fixture
def test_xlsx_path(tmp_path: Path) -> Path:
    if not HAS_OFFICE:
        pytest.skip("openpyxl not installed")
    path = tmp_path / "test.xlsx"
    wb = openpyxl.Workbook()
    ws = wb.active
    ws["A1"] = "User Email"
    ws["B1"] = "charlie@example.com"
    ws["C1"] = None
    ws["D1"] = "   "
    wb.save(path)
    return path


@pytest.fixture
def test_pptx_path(tmp_path: Path) -> Path:
    if not HAS_OFFICE:
        pytest.skip("python-pptx not installed")
    path = tmp_path / "test.pptx"
    prs = pptx.Presentation()
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = "Presentation"
    slide.placeholders[1].text = "Reach us at diana@example.com"
    slide.shapes.add_shape(pptx.enum.shapes.MSO_SHAPE.RECTANGLE, 0, 0, 100, 100)  # No text
    tb = slide.shapes.add_textbox(0, 0, 100, 100)
    tb.text = "   "  # Empty text
    prs.save(str(path))
    return path


def test_inspect_pdf(test_pdf_path: Path) -> None:
    engine = Pseudonymizer(
        policy=Policy.default(),
    )
    result = engine.inspect_file(test_pdf_path, format=FileFormat.PDF)
    assert result.statistics.detections_found >= 1
    assert any(d.entity_type == "EMAIL" for d in result.detections)


def test_inspect_docx(test_docx_path: Path) -> None:
    engine = Pseudonymizer(
        policy=Policy.default(),
    )
    result = engine.inspect_file(test_docx_path, format=FileFormat.DOCX)
    assert result.statistics.detections_found >= 1
    assert any(d.entity_type == "EMAIL" for d in result.detections)


def test_inspect_xlsx(test_xlsx_path: Path) -> None:
    engine = Pseudonymizer(
        policy=Policy.default(),
    )
    result = engine.inspect_file(test_xlsx_path, format=FileFormat.XLSX)
    assert result.statistics.detections_found >= 1
    assert any(d.entity_type == "EMAIL" for d in result.detections)


def test_inspect_pptx(test_pptx_path: Path) -> None:
    engine = Pseudonymizer(
        policy=Policy.default(),
    )
    result = engine.inspect_file(test_pptx_path, format=FileFormat.PPTX)
    assert result.statistics.detections_found >= 1
    assert any(d.entity_type == "EMAIL" for d in result.detections)


def test_process_pdf_fails(test_pdf_path: Path, tmp_path: Path) -> None:
    engine = Pseudonymizer(policy=Policy.default())
    from pseudonymize.exceptions import UnsupportedFormatError

    with pytest.raises(UnsupportedFormatError, match="inspection only"):
        engine.process_file(test_pdf_path, tmp_path / "out.pdf", format=FileFormat.PDF)
    assert not (tmp_path / "out.pdf").exists()


def test_process_docx_fails(test_docx_path: Path, tmp_path: Path) -> None:
    engine = Pseudonymizer(policy=Policy.default())
    from pseudonymize.exceptions import UnsupportedFormatError

    with pytest.raises(UnsupportedFormatError, match="inspection only"):
        engine.process_file(test_docx_path, tmp_path / "out.docx", format=FileFormat.DOCX)
    assert not (tmp_path / "out.docx").exists()
