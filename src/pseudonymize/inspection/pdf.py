from pathlib import Path

from pseudonymize.document import ContentBlock, CoordinateLocation, Document
from pseudonymize.exceptions import AdapterContractError, AdapterExecutionError

try:
    from pdfminer.high_level import extract_pages
    from pdfminer.layout import LTTextContainer

    HAS_PDF = True
except ImportError:
    HAS_PDF = False


class PDFInspectionAdapter:
    """Extracts text from PDF documents for inspection-only pipelines."""

    def __init__(self) -> None:
        if not HAS_PDF:
            raise RuntimeError(
                "The PDF adapter requires the 'pdf' extra. "
                "Install it with `pip install pseudonymize[pdf]`."
            )

    def extract(self, source: Path) -> Document:
        blocks: list[ContentBlock] = []
        try:
            with source.open("rb") as f:
                for page_index, page_layout in enumerate(extract_pages(f)):
                    for element in page_layout:
                        if isinstance(element, LTTextContainer):
                            text = element.get_text().strip()
                            if text:
                                # PDFMiner bounding box is (x0, y0, x1, y1)
                                # where y0 is distance from bottom
                                x0, y0, x1, y1 = element.bbox
                                location = CoordinateLocation(
                                    page=page_index,
                                    x0=float(x0),
                                    y0=float(y0),
                                    x1=float(x1),
                                    y1=float(y1),
                                )
                                blocks.append(
                                    ContentBlock(
                                        id=f"page-{page_index}-box-{len(blocks):06d}",
                                        text=text,
                                        location=location,
                                    )
                                )
        except Exception:
            raise AdapterExecutionError("input adapter failed while reading the PDF") from None

        metadata = {"format": "pdf"}
        return Document("file", tuple(blocks), metadata)

    def render(self, document: Document) -> bytes:
        raise AdapterContractError(
            "PDF format-preserving rendering is not yet supported. "
            "PDF extraction is for inspection only."
        )
