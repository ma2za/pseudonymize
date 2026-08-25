from io import BytesIO
from pathlib import Path

from pseudonymize.document import ContentBlock, CoordinateLocation, Document
from pseudonymize.exceptions import AdapterExecutionError

try:
    import pymupdf

    HAS_PDF = True
except ImportError:
    HAS_PDF = False

try:
    import pytesseract

    HAS_OCR = True
except ImportError:
    HAS_OCR = False


class PDFInspectionAdapter:
    """Extracts and format-preserves PDF documents using secure redaction."""

    def __init__(self) -> None:
        if not HAS_PDF:
            raise RuntimeError(
                "The PDF adapter requires the 'pdf' extra. "
                "Install it with `pip install pseudonymize[pdf]`."
            )
        self._source_path: Path | None = None

    def extract(self, source: Path) -> Document:
        blocks: list[ContentBlock] = []
        self._source_path = source
        try:
            doc = pymupdf.open(source)
            for page_index, page in enumerate(doc):
                # get_text("blocks") returns tuples: (x0, y0, x1, y1, "text", block_no, block_type)
                # block_type == 0 means text, 1 means image
                page_blocks = page.get_text("blocks")
                page_had_text = False
                for b in page_blocks:
                    if len(b) >= 7 and b[6] == 0:
                        x0, y0, x1, y1, text, block_no, _ = b
                        text = text.strip()
                        if text:
                            page_had_text = True
                            location = CoordinateLocation(
                                page=page_index,
                                x0=float(x0),
                                y0=float(y0),
                                x1=float(x1),
                                y1=float(y1),
                            )
                            blocks.append(
                                ContentBlock(
                                    id=f"page-{page_index}-block-{block_no:06d}",
                                    text=text,
                                    location=location,
                                )
                            )

                # Fallback to OCR if the page has no extractable text and OCR is available
                if not page_had_text and HAS_OCR:
                    dpi = 300
                    pix = page.get_pixmap(dpi=dpi)
                    img = pix.pil_image()

                    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)

                    # Tesseract coordinates are in pixels at the specified DPI.
                    # PDF coordinates are in points (72 points per inch).
                    scale = 72.0 / dpi

                    n_boxes = len(data["text"])
                    for i in range(n_boxes):
                        text = data["text"][i].strip()
                        if text:
                            # Tesseract bounding box
                            left = data["left"][i]
                            top = data["top"][i]
                            width = data["width"][i]
                            height = data["height"][i]

                            # Convert to PDF points
                            x0 = left * scale
                            y0 = top * scale
                            x1 = (left + width) * scale
                            y1 = (top + height) * scale

                            location = CoordinateLocation(
                                page=page_index,
                                x0=float(x0),
                                y0=float(y0),
                                x1=float(x1),
                                y1=float(y1),
                            )
                            blocks.append(
                                ContentBlock(
                                    id=f"page-{page_index}-ocr-{i:06d}",
                                    text=text,
                                    location=location,
                                )
                            )

            doc.close()
        except Exception:
            raise AdapterExecutionError("input adapter failed while reading the PDF") from None

        metadata = {"format": "pdf"}
        return Document("file", tuple(blocks), metadata)

    def render(self, document: Document) -> bytes:
        if not self._source_path:
            raise AdapterExecutionError("Cannot render before extraction")

        try:
            doc = pymupdf.open(self._source_path)

            page_blocks: dict[int, list[ContentBlock]] = {}
            for block in document.blocks:
                loc = block.location
                if isinstance(loc, CoordinateLocation):
                    page_blocks.setdefault(loc.page, []).append(block)

            for page_index, page in enumerate(doc):
                if page_index in page_blocks:
                    for block in page_blocks[page_index]:
                        loc = block.location
                        if not isinstance(loc, CoordinateLocation):
                            continue

                        rect = pymupdf.Rect(loc.x0, loc.y0, loc.x1, loc.y1)
                        # Add redaction annotation with overlay text
                        page.add_redact_annot(rect, text=block.text, fill=(0, 0, 0))

                    # Apply redactions to securely remove the underlying text
                    page.apply_redactions()

            # Clean metadata
            doc.set_metadata(
                {
                    "author": "pseudonymize",
                    "creator": "pseudonymize",
                    "producer": "pseudonymize",
                    "title": "Sanitized Document",
                    "subject": "",
                }
            )

            out = BytesIO()
            # Save securely to purge unused objects and streams
            doc.save(out, garbage=4, deflate=True, clean=True)
            doc.close()
            return out.getvalue()
        except Exception:
            raise AdapterExecutionError("output adapter failed while rendering the PDF") from None
