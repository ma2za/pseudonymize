from io import BytesIO
from pathlib import Path
from typing import Any

from pseudonymize.document import ContentBlock, Document, StructuralLocation
from pseudonymize.exceptions import AdapterExecutionError

try:
    import docx
    import openpyxl
    import pptx

    HAS_OFFICE = True
except ImportError:
    HAS_OFFICE = False


class OfficeInspectionAdapter:
    """Extracts and format-preserves Office documents (DOCX, XLSX, PPTX)."""

    def __init__(self, format_hint: str) -> None:
        if not HAS_OFFICE:
            raise RuntimeError(
                "The Office adapter requires the 'office' extra. "
                "Install it with `pip install pseudonymize[office]`."
            )
        self.format_hint = format_hint.lower()
        if self.format_hint not in ("docx", "xlsx", "pptx"):
            raise ValueError(f"Unsupported Office format hint: {format_hint}")
        self._doc: Any = None

    def extract(self, source: Path) -> Document:
        blocks: list[ContentBlock] = []
        try:
            if self.format_hint == "docx":
                self._extract_docx(source, blocks)
            elif self.format_hint == "xlsx":
                self._extract_xlsx(source, blocks)
            elif self.format_hint == "pptx":
                self._extract_pptx(source, blocks)
        except Exception:
            raise AdapterExecutionError(
                f"input adapter failed while reading the {self.format_hint.upper()} document"
            ) from None

        metadata = {"format": self.format_hint}
        return Document("file", tuple(blocks), metadata)

    def _extract_docx(self, source: Path, blocks: list[ContentBlock]) -> None:
        self._doc = docx.Document(str(source))
        for para_index, para in enumerate(self._doc.paragraphs):
            text = para.text.strip()
            if text:
                blocks.append(
                    ContentBlock(
                        id=f"para-{para_index:06d}",
                        text=text,
                        location=StructuralLocation(("paragraph", para_index)),
                    )
                )
        for table_index, table in enumerate(self._doc.tables):
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
        self._doc = openpyxl.load_workbook(filename=source, data_only=True)
        for sheet_index, sheet_name in enumerate(self._doc.sheetnames):
            sheet = self._doc[sheet_name]
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
        self._doc = pptx.Presentation(str(source))
        for slide_index, slide in enumerate(self._doc.slides):
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
        if not self._doc:
            raise AdapterExecutionError("Cannot render before extraction")

        try:
            if self.format_hint == "docx":
                self._render_docx(document)
            elif self.format_hint == "xlsx":
                self._render_xlsx(document)
            elif self.format_hint == "pptx":
                self._render_pptx(document)
        except Exception:
            raise AdapterExecutionError(
                f"output adapter failed while rendering the {self.format_hint.upper()} document"
            ) from None

        out = BytesIO()
        self._doc.save(out)
        return out.getvalue()

    def _clean_core_properties(self, core_properties: Any) -> None:
        """Sanitize common author and modification metadata."""
        if hasattr(core_properties, "author"):
            core_properties.author = "pseudonymize"
        if hasattr(core_properties, "last_modified_by"):
            core_properties.last_modified_by = "pseudonymize"
        if hasattr(core_properties, "comments"):
            core_properties.comments = ""
        if hasattr(core_properties, "title"):
            core_properties.title = "Sanitized Document"
        if hasattr(core_properties, "subject"):
            core_properties.subject = ""

    def _render_docx(self, document: Document) -> None:
        self._clean_core_properties(self._doc.core_properties)
        for block in document.blocks:
            loc = block.location
            if not isinstance(loc, StructuralLocation):
                continue
            path = loc.path
            if len(path) == 2 and path[0] == "paragraph":
                para_index = int(path[1])
                self._doc.paragraphs[para_index].text = block.text
            elif len(path) == 6 and path[0] == "table":
                table_index = int(path[1])
                row_index = int(path[3])
                col_index = int(path[5])
                self._doc.tables[table_index].rows[row_index].cells[col_index].text = block.text

    def _render_xlsx(self, document: Document) -> None:
        if hasattr(self._doc, "properties"):
            self._clean_core_properties(self._doc.properties)
            # XLSX creator properties
            if hasattr(self._doc.properties, "creator"):
                self._doc.properties.creator = "pseudonymize"

        for block in document.blocks:
            loc = block.location
            if not isinstance(loc, StructuralLocation):
                continue
            path = loc.path
            if len(path) == 6 and path[0] == "sheet":
                sheet_name = str(path[1])
                row_index = int(path[3])
                col_index = int(path[5])
                # openpyxl uses 1-based indexing
                self._doc[sheet_name].cell(
                    row=row_index + 1, column=col_index + 1, value=block.text
                )

    def _render_pptx(self, document: Document) -> None:
        self._clean_core_properties(self._doc.core_properties)
        for block in document.blocks:
            loc = block.location
            if not isinstance(loc, StructuralLocation):
                continue
            path = loc.path
            if len(path) == 4 and path[0] == "slide":
                slide_index = int(path[1])
                shape_index = int(path[3])
                self._doc.slides[slide_index].shapes[shape_index].text = block.text
