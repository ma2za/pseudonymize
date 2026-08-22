from pathlib import Path

from pseudonymize.document import ContentBlock, Document, StructuralLocation
from pseudonymize.exceptions import AdapterContractError, AdapterExecutionError

try:
    import docx
    import openpyxl
    import pptx

    HAS_OFFICE = True
except ImportError:
    HAS_OFFICE = False


class OfficeInspectionAdapter:
    """Extracts text from Office documents (DOCX, XLSX, PPTX) for inspection."""

    def __init__(self, format_hint: str) -> None:
        if not HAS_OFFICE:
            raise RuntimeError(
                "The Office adapter requires the 'office' extra. "
                "Install it with `pip install pseudonymize[office]`."
            )
        self.format_hint = format_hint.lower()
        if self.format_hint not in ("docx", "xlsx", "pptx"):
            raise ValueError(f"Unsupported Office format hint: {format_hint}")

    def extract(self, source: Path) -> Document:
        blocks: list[ContentBlock] = []
        try:
            if self.format_hint == "docx":
                self._extract_docx(source, blocks)
            elif self.format_hint == "xlsx":
                self._extract_xlsx(source, blocks)
            elif self.format_hint == "pptx":
                self._extract_pptx(source, blocks)
        except Exception as e:
            raise AdapterExecutionError(f"Failed to read Office document: {e}") from e

        metadata = {"format": self.format_hint}
        return Document("file", tuple(blocks), metadata)

    def _extract_docx(self, source: Path, blocks: list[ContentBlock]) -> None:
        doc = docx.Document(str(source))
        for para_index, para in enumerate(doc.paragraphs):
            text = para.text.strip()
            if text:
                blocks.append(
                    ContentBlock(
                        id=f"para-{para_index:06d}",
                        text=text,
                        location=StructuralLocation(("paragraph", para_index)),
                    )
                )
        # We can also extract tables if needed, for simplicity we stick to paragraphs and tables
        for table_index, table in enumerate(doc.tables):
            for row_index, row in enumerate(table.rows):
                for col_index, cell in enumerate(row.cells):
                    text = cell.text.strip()
                    if text:
                        blocks.append(
                            ContentBlock(
                                id=f"table-{table_index:06d}-row-{row_index:06d}-col-{col_index:06d}",
                                text=text,
                                location=StructuralLocation(
                                    ("table", table_index, "row", row_index, "column", col_index)
                                ),
                            )
                        )

    def _extract_xlsx(self, source: Path, blocks: list[ContentBlock]) -> None:
        wb = openpyxl.load_workbook(filename=source, data_only=True)
        for sheet_index, sheet_name in enumerate(wb.sheetnames):
            sheet = wb[sheet_name]
            for row_index, row in enumerate(sheet.iter_rows(values_only=True)):
                for col_index, cell_value in enumerate(row):
                    if cell_value is not None:
                        text = str(cell_value).strip()
                        if text:
                            blocks.append(
                                ContentBlock(
                                    id=f"sheet-{sheet_index:06d}-row-{row_index:06d}-col-{col_index:06d}",
                                    text=text,
                                    location=StructuralLocation(
                                        ("sheet", sheet_name, "row", row_index, "column", col_index)
                                    ),
                                )
                            )

    def _extract_pptx(self, source: Path, blocks: list[ContentBlock]) -> None:
        prs = pptx.Presentation(str(source))
        for slide_index, slide in enumerate(prs.slides):
            for shape_index, shape in enumerate(slide.shapes):
                if hasattr(shape, "text") and shape.text:
                    text = shape.text.strip()
                    if text:
                        blocks.append(
                            ContentBlock(
                                id=f"slide-{slide_index:06d}-shape-{shape_index:06d}",
                                text=text,
                                location=StructuralLocation(
                                    ("slide", slide_index, "shape", shape_index)
                                ),
                            )
                        )

    def render(self, document: Document) -> bytes:
        raise AdapterContractError(
            f"{self.format_hint.upper()} format-preserving rendering is not yet supported. "
            "Office extraction is for inspection only."
        )
